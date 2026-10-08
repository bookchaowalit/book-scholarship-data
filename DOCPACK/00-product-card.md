---
title: Book Scholarship Data — Product Card
doc_id: CARD-book-scholarship-data
doc_type: product-card
verdict: showcase
version: 0.1
date: 2026-10-08
status: ร่างเพื่อพิจารณา
owner: Product owner (Book Dev)
---

# Book Scholarship Data — Product Card

## 1. สรุปคุณค่าในหนึ่งประโยค

ช่วยผู้เรียนและทีมแนะแนวค้นหาทุนการศึกษาที่ยังเปิดรับ แยกตามระดับการศึกษาและความครอบคลุมค่าใช้จ่าย โดยไม่สร้างข้อมูลที่ไม่รู้ให้กลายเป็นข้อเท็จจริง

## 2. ปัญหาและผู้ใช้เป้าหมาย

- ข้อมูลทุนกระจัดกระจาย เงื่อนไขซับซ้อน และสับสนระหว่าง 'ไดเรกทอรีโครงการ' กับ 'ทุนจริง'
- ผู้ใช้เป้าหมายตาม README: บุคคลและทีมเล็กที่หาทุนการศึกษา **[สมมติฐาน]** ไม่มีหลักฐานผู้ใช้จริง

## 3. สิ่งที่ทำได้จริงตอนนี้

- CLI `contract` (v1 สำหรับ demo, v2 สำหรับข้อมูลที่ capture จริง), `demo --open-only`, `validate` เลือก schema ตาม `schema_version`
- schema `scholarship.v2` แยก unknown ออกจาก false และแยก program directory ออกจาก award จริง
- มี source policy ทางการ 4 แหล่งของสหราชอาณาจักร (undergraduate student finance, 16-19 bursary, free courses, university scholarships) + policy หลัก; capture แบบสั่งด้วยมือ
- test 5 ไฟล์ offline รวม text extraction

## 4. หลักฐานสถานะ

- Stack: Python
- Commits: 12 (แรก 2026-09-09 → ล่าสุด 2026-10-01), branch `main`; working tree สะอาด
- Source: 9 ไฟล์ / 846 บรรทัด; test 5 ไฟล์
- CI: 1 workflow
- Deploy config: ไม่มี
- Live URL: ไม่พบใน repo
- โครงสร้างไฟล์เหมือนกับ repo อื่นอีก 12 ตัวในตระกูลเดียวกัน (structure signature เดียวกัน)

## 5. คุณค่าและจุดต่าง

- จุดต่างคือ schema v2 ที่ซื่อตรงต่อความไม่แน่นอนของข้อมูล ซึ่งเว็บรวมทุนทั่วไปมักไม่ทำ
- แหล่งข้อมูลทั้งหมดเป็นของสหราชอาณาจักร จึงไม่ตรงกับผู้ใช้ไทยโดยตรง
- มุมรายได้/การใช้ซ้ำ: เนื้อหา SEO หรือบริการแนะแนวทุน **[สมมติฐาน]**

## 6. ช่องว่างสำคัญ

- ไม่มีแหล่งทุนไทยหรือเอเชีย
- ยังไม่มีผู้ใช้ปลายทาง: README ระบุว่าไม่มี scheduler, hosted API หรือ consumer integration (`Consumers: integration planned`)
- โครงเดียวกับอีก 12 repo ในตระกูล intake ต้นทุนดูแลซ้ำซ้อน

## 7. คำตัดสิน

**showcase** — เป็นตัวที่ก้าวหน้าที่สุดในกลุ่มนี้ (schema v2, หลายแหล่ง) และเป็นหลักฐานงาน data contract ที่ดี แต่ยังไม่มีผู้ใช้และไม่มีแหล่งที่ตรงตลาดของเจ้าของ

จะเป็น `invest` เมื่อเพิ่มแหล่งทุนไทยและมีช่องทางให้ผู้ใช้จริงเห็นผล (เช่นหน้า listing หรือ digest); ถ้ารวมตระกูลเป็นแพ็กเกจเดียวให้เปลี่ยนเป็น `merge`

## 8. ขั้นต่อไป

1. ใช้ schema v2 ของ repo นี้เป็นต้นแบบสำหรับตระกูล intake ทั้งหมด
2. สำรวจแหล่งทุนไทยที่เปิดเผยและอนุญาตให้ใช้ข้อมูล
3. ตัดสินใจเรื่องรวม 13 repo เป็นแพ็กเกจเดียว

## การอนุมัติ

| บทบาท | สถานะ | วันที่ | ลงนาม |
|---|---|---|---|
| Product owner (Book Dev) | รอพิจารณา | — | ________ |

## แหล่งข้อมูล

- `README.md`
- `PRODUCT.md`
- `src/book_scholarship_data/schema-v2.json`
- `src/book_scholarship_data/`
- `tests/`
