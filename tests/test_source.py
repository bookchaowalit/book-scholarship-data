import base64
import json
import unittest
from book_scholarship_data.capture import normalize
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

if __name__=='__main__': unittest.main()
