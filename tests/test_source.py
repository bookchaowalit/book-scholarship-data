import base64
import json
import unittest
from pathlib import Path
from urllib.parse import urlsplit

from book_scholarship_data.capture import normalize
from book_scholarship_data.capture import source_config as capture_source
from book_scholarship_data.cli import resource, validate


class SourceTests(unittest.TestCase):
    def raw(self):
        source=resource('source.json')
        if source['access']=='html': return b'<h1>Chevening in Thailand</h1><p>Open for applications until 6 October 2026, at 11:00 (UTC)</p>'
        if source['access']=='github-api': return json.dumps({'encoding':'base64','name':'about-github-education-for-students.md','content':base64.b64encode(b'title: About GitHub Education for students').decode()}).encode()
        return json.dumps({'base_path':source['source_url'].removeprefix('https://www.gov.uk'),'title':'Universal Credit' if source['domain']=='benefit' else 'Apply for innovation funding','details':{}}).encode()

    def test_parse_and_validate_v2(self):
        source=resource('source.json')
        data=normalize(self.raw(),source,'2026-09-07T00:00:00Z')
        for item in data['items']: item['provenance'].update(raw_object_key='landing/test',bronze_manifest_key='control/manifests/test')
        self.assertEqual(validate(data)['schema_version'],source['schema_version'])
        self.assertTrue(any(v is None for v in data['items'][0]['terms'].values()))

    def test_unknown_terms_not_false(self):
        data=normalize(self.raw(),resource('source.json'),'2026-09-07T00:00:00Z')
        self.assertNotIn(False,data['items'][0]['terms'].values())

    def test_source_drift_rejected(self):
        with self.assertRaises((ValueError,KeyError)):
            normalize(b'{}',resource('source.json'),'2026-09-07T00:00:00Z')

    def test_missing_lineage_rejected(self):
        data=normalize(self.raw(),resource('source.json'),'2026-09-07T00:00:00Z')
        with self.assertRaises(ValueError): validate(data)

    def test_v1_still_supported(self):
        self.assertEqual(validate(resource('demo.json'))['data_status'],'fixture')

    def test_exact_deadline_or_unknown(self):
        source=resource('source.json')
        item=normalize(self.raw(),source,'2026-09-07T00:00:00Z')['items'][0]
        if source['domain']=='scholarship':
            self.assertEqual(item['deadline']['at'],'2026-10-06T11:00:00Z')
            self.assertEqual(item['status'],'open')
            later=normalize(self.raw(),source,'2026-10-06T11:00:00Z')['items'][0]
            self.assertEqual(later['status'],'closed')
        else:
            self.assertEqual(item['deadline']['kind'],'unknown')
            self.assertEqual(item['status'],'unknown')
    def test_generic_govuk_sources_normalize(self):
        catalog = json.loads((Path(__file__).resolve().parents[1] / 'sources.json').read_text(encoding='utf-8'))
        generic = [capture_source(i) for i in catalog['enabled_sources']]
        generic = [s for s in generic if s.get('generic_html')]
        self.assertTrue(generic)
        for source in generic:
            with self.subTest(source=source['id']):
                body = {'base_path': urlsplit(source['fetch_url']).path.removeprefix('/api/content'), 'title': source['title'],
                        'description': '', 'details': {'body': ' '.join(source['required_markers'])}}
                data = normalize(json.dumps(body).encode(), source, '2026-09-08T00:00:00Z')
                item = data['items'][0]
                item['provenance'].update(raw_object_key='landing/test', bronze_manifest_key='control/manifests/test')
                self.assertEqual(item['category'], source['category'])
                self.assertEqual(item['status'], 'unknown')
                self.assertEqual(item['deadline'], {'kind': 'unknown', 'at': None})
                self.assertEqual(item['terms']['study_level'], source['normalized_terms']['study_level'])
                self.assertEqual(validate(data)['schema_version'], 'scholarship.v2')

                drifted = dict(body, details={'body': 'unrelated guidance'})
                with self.assertRaises(ValueError):
                    normalize(json.dumps(drifted).encode(), source, '2026-09-08T00:00:00Z')
                misrouted = dict(body, base_path='/guidance/some-other-page')
                with self.assertRaises(ValueError):
                    normalize(json.dumps(misrouted).encode(), source, '2026-09-08T00:00:00Z')

    def test_chevening_closed_notice(self):
        raw = b'<h1>Chevening in Thailand</h1><p>Applications are closed.</p>'
        item = normalize(raw, resource('source.json'), '2026-09-07T00:00:00Z')['items'][0]
        self.assertEqual(item['status'], 'closed')
        self.assertEqual(item['deadline'], {'kind': 'unknown', 'at': None})
        self.assertEqual(item['id'], 'chevening-thailand')

    def chevening(self, until):
        return ('<h1>Chevening in Thailand</h1><p>Open for applications until ' + until + ' (UTC)</p>').encode()

    def test_chevening_utc_cutoff_across_offsets(self):
        source=resource('source.json')
        self.assertEqual(source['access'],'html')
        raw=self.chevening('6 October 2026, at 11:00')
        cases={'2026-10-06T10:59:59Z':'open','2026-10-06T11:00:00Z':'closed',
               '2026-10-06T17:59:59+07:00':'open','2026-10-06T18:00:00+07:00':'closed',
               '2026-10-06T06:59:59-04:00':'open','2026-10-06T07:00:00-04:00':'closed'}
        for checked_at,status in cases.items():
            with self.subTest(checked_at=checked_at):
                item=normalize(raw,source,checked_at)['items'][0]
                self.assertEqual(item['deadline'],{'kind':'fixed','at':'2026-10-06T11:00:00Z'})
                self.assertEqual(item['status'],status)

    def test_chevening_rejects_naive_clock_and_unknown_months(self):
        source=resource('source.json')
        with self.assertRaises(ValueError):
            normalize(self.chevening('6 October 2026, at 11:00'),source,'2026-10-06T11:00:00')
        for until in ('6 Octobre 2026, at 11:00','6 October 2026, at 24:00','31 September 2026, at 11:00'):
            with self.subTest(until=until),self.assertRaises(ValueError):
                normalize(self.chevening(until),source,'2026-09-07T00:00:00Z')
        item=normalize(self.chevening('6 OCTOBER 2026, at 11:00'),source,'2026-09-07T00:00:00Z')['items'][0]
        self.assertEqual(item['deadline']['at'],'2026-10-06T11:00:00Z')


if __name__=='__main__': unittest.main()
