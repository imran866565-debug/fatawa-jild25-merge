#!/usr/bin/env python3
"""Merge Jild 25 tashreeh chunks into jild-25.json.

Re-runnable: reads every jild-25-chunk-*.json listed in the manifest,
merges in chunk order, validates (unique ids, page coverage, empty
jawab allow-list), writes jild-25.json, and updates the manifest statuses.

INPUT (verified on disk by the parent):
  12 chunk files (no splits), 191 chunk items, volume_id 37. Source
  export ~/workspace/fatawa-app/content/jild-25.json: 608 unique pages
  pp. 5-658. Gaps (46, nothing invented): pp. 11-52 (42), 76, 304,
  401, 402 — every gap listed in the manifest's source_gaps and in
  each chunk's missing_pages (Jild 17 lesson), except pp. 304 and
  401-402 which lie BETWEEN chunks (304 between chunk 05 end p. 303
  and chunk 06 start p. 305; 401-402 between chunk 07 end p. 400 and
  chunk 08 start p. 403) and are inside NO chunk's span (listed in
  the manifest as inter_chunk_gaps). Validate against the chunk
  items' page union (608 pages), NOT range arithmetic. Lesson 119 is
  entirely absent from the export (lessons jump 118 -> 120).

COMBINE RULES (5 cases; parts ordered by min page; pages = UNION of
all parts' pages; notes = all parts' notes; start_page = min page;
sawal from the FIRST part for every combine — no concatenation case
in this volume):
  masala 25:   SAME-ID, sawal from first. Chunk 02 [107-160]
               (sawal 1,134, jawab 46,631) + chunk 03 [161-203]
               (empty sawal, jawab 24,457) -> [107-203] (97 pages).
               Sawal 1,134, jawab 71,088. Risala 121 (الفقہ التسجیلی
               فی عجین النارجیلی) is ONE mas'ala (25); closes p. 203
               "(رسالہ الفقہ التسجیلی ختم ہوا)".
  masala 113:  SAME-ID, sawal from first. Chunk 06 [354-356]
               (sawal 1,692, jawab 2,490) + chunk 07 [357] (empty
               sawal, jawab 821) -> [354-357]. Sawal 1,692, jawab
               3,311. Mas'ala 114 begins on p. 357 after this item's
               tail (verified from source).
  masala 142:  SAME-ID, sawal from first (مرض الموت کی تعریف).
               Chunk 08 [457-458] (sawal 142, jawab 2,081) + chunk
               09 [459] (empty sawal, jawab 299) -> [457-459].
               Sawal 142, jawab 2,380. Mas'ala 143 begins mid-page
               459 after this item's tail (verified from source).
  masala 157:  SAME-ID, sawal from first. Chunk 09 [502] (sawal
               1,382, jawab EMPTY — split head) + chunk 10 [503]
               (empty sawal, jawab 2,032) -> [502, 503]. Sawal
               1,382, jawab 2,032. Question ends p. 502; jawab opens
               p. 503 with "الجواب:". Mas'ala 158 begins mid-page
               503 after this item ends.
  masala 158:  RISALA MEGA-COMBINE (20 parts -> 1). The Chief Court
               Bahawalpur case (mas'ala 158, "مسئہ ۱۵۸" as printed)
               is ONE mas'ala spanning chunks 10, 11 and 12. Its
               jawab (Ala Hazrat's own, beginning bottom of p. 542)
               follows the four-part plan laid out on p. 543: اولاً
               افادہ مسائل (+ تفریعات)، ثانیاً پانچ سوالاتِ حال،
               ثالثاً سات سوالاتِ سابق، رابعاً حکمِ اخیر.
               Part A: chunk 10 'jild25-masala-158' [503-543] (sawal
               58,626, jawab 2,272 — case material + jawab intro
               only). Part B: chunk 11 'jild25-masala-158' [544-600]
               (empty sawal, jawab 81,665 — افادہ اولٰی–ثانیہ عشر,
               تفریعات ۱–۷۰, فوائد ۱–۱۲ of افادہ خامسہ + فوائد ۱۳–۱۴
               of افادہ ثانیہ عشر). Parts C-T: chunk 12's 18
               discussion items (ALL sawal EMPTY, jawabs 844, 1093,
               1140, 753, 1021, 3968, 6005, 1254, 1414, 1857, 1645,
               2226, 2407, 953, 6960, 2107, 2365, 3081 = 41,093
               total) -> merged [503-630] (128 pages), sawal 58,626
               (the only non-empty sawal), jawab 125,030 (2,272 +
               81,665 + 41,093). Absorb all 18 chunk-12 discussion
               ids into 'jild25-masala-158' — they must NOT remain
               as separate items. Evidence (verified by the
               coordinator against jild-25.json): pp. 601-630 contain
               NO numbered مسئلہ heading at all (the only heading in
               that range is مسئلہ ۱۵۹ on p. 630, char 535); p. 630
               head closes this jawab with "وباﷲ التوفیق واﷲ تعالٰی
               اعلم وصلی اﷲ تعالٰی علٰی سیدنا ومولٰنا محمد واٰلہٖ
               وصحبہٖ اجمعین وبارك وسلم اٰمین والحمدﷲ ربّ
               العٰلمین"; p. 601 head continues the رد discussion
               mid-sentence. The lesson-126 heading "افادات
               والتفریعات" at the top of p. 544 is INSIDE this
               jawab, not a separate lesson/item. Masala-159 begins
               mid-page 630 and is a separate item.
After all 5 combines: 191 - 23 = 168 items covering 608 unique pages.

RENAMES: NO merge-time renames. One rename was already applied in
the chunk files and must NOT be re-applied: printed "مسئلہ ۲۹" on
p. 380 -> 'jild25-masala-129' [380-381] (chunk 07; sequence 128
before, 130 on p. 381 proves 129; note recorded in the chunk file).
Do NOT globally normalise bare ids.

WARNING — the 129/29 distinction (checked by the coordinator against
ALL chunk files, and verified by the parent): a GENUINE
'jild25-masala-29' [204-205] exists in chunk 03 (a real mas'ala 29
in the al-Fiqh al-Tasjili sequence, sawal 438, jawab 963). It is a
DIFFERENT item from the renamed 'jild25-masala-129' [380-381] and
must be kept as-is. Do NOT confuse the two; do NOT rename it; do NOT
merge it with masala-129. The merged file must contain BOTH
'jild25-masala-29' [204-205] AND 'jild25-masala-129' [380-381] as
separate items. (This is the Jild 24 masala-279 lesson.)

EMPTY-JAWAB ALLOW-LIST: after the combines, exactly ONE item has an
empty tashreeh_jawab: 'jild25-masala-139a' [437-441] (sawal 8,557
chars, jawab EMPTY). This is BY DESIGN, not a translator omission:
its 11 questions are answered jointly in 139(b)'s answer (pp.
443-452), where "جواب سوال ششم" and "جواب سوال ہشتم" expressly
answer (a)'s Q6 and Q8 and "اوّلاً تا سابعاً" settles the rest. This
is NOT a bare-الجواب case. The merge script allow-lists exactly
this one item. All other items must have non-empty jawab (the
split-head empty jawab — masala-157 [502] — is resolved by combine
4). Empty sawal after merge: exactly 4 (pesh-lafz, kitab-al-wasaya,
masala-126, masala-129 — all by design).

DO-NOT-COMBINES: Masala-66 is COMPLETE on p. 259 (verified from
source: question + full answer ending "واﷲ تعالٰی اعلم وعلمہ جل مجدہ
اتم واحکم" on p. 259; p. 260 opens mas'ala 67). Chunk 05 correctly
has NO masala-66 item. Do NOT create a phantom masala-66 half.
Risala 125 (الشرعۃ البھیۃ فی تحدید الوصیۃ) closes on p. 432
("رسالہ الشرعۃ البھیۃ فی تحدید الوصیۃ (۱۳۱۷ھ) ختم ہوا") — masala-135
[403-432] IS the complete risala. Pp. 433+ are further masail of
lesson 125, not a continuation of the risala. Masala-139a/139b share
p. 441 (139b heading mid-page 441, verified from source). 139a
keeps its empty jawab (allow-listed above); 139b is a separate item.
Masala-134 [389-400]: jawab INCOMPLETE in the source — ends
mid-sentence on p. 400. Masala-100 [302]: jawab TRUNCATED in the
source. Masala-101 [302]: printed footnote "یہ فتوٰی ناتمام ہے۔
عبدالمبین نعمانی۔" Grouped items kept as single items (first
number's id): masala-26-28, 35-36, 40-42, 62-63, 71-73, 74-75,
77-78, 80-83, 89-91, 96-97, 152-153, 176-177. Shared pages by design
(one mas'ala ends, the next begins on the same page): p. 305
(heading item + masala-103), p. 441 (139a/139b), p. 459 (142 tail /
143), p. 503 (157 tail / 158), p. 630 (158 tail / 159). Page union
must still be exactly 608. Volume ends p. 658 with masala-183's
jawab and then the publisher's closing note: «جلد ۲۵ کتاب المداینات
سے شروع ہوکر کتاب الوصایا کے عنوان پر ختم ہوئی، جلد ۲۶ ان شاء اللہ
کتاب الفرائض سے شروع ہوگی۔» — recorded in masala-183's notes. No
separate khatima item. Last item 'jild25-masala-183' [656-658].
PUA-garbled Quran pages: 4 — p. 247 (masala-59), p. 251 (masala-60),
p. 267 (masala-70), p. 281 (masala-80-83). Flagged in item notes
only, never reconstructed. No U+FFFD pages.

SORT: merged items are sorted by start_page for the final file.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

# result id -> list of selectors, in page order.
# Selector forms:
#   ('id', sid)            — every item with this id (1 or 2 halves)
#   ('id_start', sid, sp)  — the item with this id starting at page sp
COMBINES = {
    'jild25-masala-25': [
        ('id', 'jild25-masala-25'),
    ],
    'jild25-masala-113': [
        ('id', 'jild25-masala-113'),
    ],
    'jild25-masala-142': [
        ('id', 'jild25-masala-142'),
    ],
    'jild25-masala-157': [
        ('id', 'jild25-masala-157'),
    ],
    'jild25-masala-158': [
        ('id', 'jild25-masala-158'),
        ('id', 'jild25-p598-faida-14'),
        ('id', 'jild25-p601-faida-15'),
        ('id', 'jild25-p601-faida-16'),
        ('id', 'jild25-p602-faida-17'),
        ('id', 'jild25-p603-faida-18'),
        ('id', 'jild25-p603-faida-19'),
        ('id', 'jild25-p608-faida-20'),
        ('id', 'jild25-p613-faida-21'),
        ('id', 'jild25-p614-faida-22'),
        ('id', 'jild25-p616-faida-23'),
        ('id', 'jild25-p617-faida-24'),
        ('id', 'jild25-p617-faida-25'),
        ('id', 'jild25-p619-faida-26'),
        ('id', 'jild25-p621-faida-27'),
        ('id', 'jild25-p622-tafriaat'),
        ('id', 'jild25-p626-jawab-chief-court'),
        ('id', 'jild25-p627-jawab-jajji-khanpur'),
        ('id', 'jild25-p628-hukm-akheer'),
    ],
}

# Sawal handling per combined id (default: sawal from the first part,
# sorted by min page). Every combine in this volume is sawal-from-
# first — there is NO concatenation case. (masala-158's first part by
# min page is chunk 10 [503-543] with sawal 58,626 — the only
# non-empty sawal among its 20 parts.)
SAWAL_RULES = {}

# No merge-time renames in this volume. The one rename (printed 29
# p. 380 -> masala-129) was already applied in the chunk files and is
# asserted present below. Kept empty deliberately.
RENAMES = {}

# Applied-in-chunk renames (already in the chunk files — must exist
# after merging, never re-applied).
RENAMED_IN_CHUNK = ['jild25-masala-129']

# Expected pages for every combined item (spot-check anchors).
EXPECTED_COMBINED_PAGES = {
    'jild25-masala-25': list(range(107, 204)),
    'jild25-masala-113': [354, 355, 356, 357],
    'jild25-masala-142': [457, 458, 459],
    'jild25-masala-157': [502, 503],
    'jild25-masala-158': list(range(503, 631)),
}

# Expected sawal/jawab char counts for every combined item.
# masala-25 jawab: 46631 + 24457 = 71088
# masala-113 jawab: 2490 + 821 = 3311
# masala-142 jawab: 2081 + 299 = 2380
# masala-157 jawab: 0 + 2032 = 2032
# masala-158 jawab: 2272 + 81665 + 41093 = 125030
EXPECTED_COMBINED_TEXT = {
    'jild25-masala-25': (1134, 71088),
    'jild25-masala-113': (1692, 3311),
    'jild25-masala-142': (142, 2380),
    'jild25-masala-157': (1382, 2032),
    'jild25-masala-158': (58626, 125030),
}

# The ids absorbed by the masala-158 mega-combine (must be gone after).
ABSORBED = [
    'jild25-p598-faida-14',
    'jild25-p601-faida-15',
    'jild25-p601-faida-16',
    'jild25-p602-faida-17',
    'jild25-p603-faida-18',
    'jild25-p603-faida-19',
    'jild25-p608-faida-20',
    'jild25-p613-faida-21',
    'jild25-p614-faida-22',
    'jild25-p616-faida-23',
    'jild25-p617-faida-24',
    'jild25-p617-faida-25',
    'jild25-p619-faida-26',
    'jild25-p621-faida-27',
    'jild25-p622-tafriaat',
    'jild25-p626-jawab-chief-court',
    'jild25-p627-jawab-jajji-khanpur',
    'jild25-p628-hukm-akheer',
]

# The only items allowed to keep an empty sawal after merging
# (all by design).
EMPTY_SAWAL_ALLOWED = {
    'jild25-pesh-lafz',
    'jild25-kitab-al-wasaya',
    'jild25-masala-126',
    'jild25-masala-129',
}

# The ONLY item allowed to keep an empty tashreeh_jawab after merging:
# BY DESIGN — its 11 questions are answered jointly in 139(b)'s
# answer (pp. 443-452). Verified by the parent from the chunk files.
# Every other item must have a non-empty jawab.
EMPTY_JAWAB_ALLOWED = {'jild25-masala-139a'}

# BOTH masala-29 and masala-129 must exist as SEPARATE items (see
# WARNING in the docstring above): the genuine masala-29 [204-205]
# and the renamed masala-129 [380-381].
BOTH_29_AND_129 = {
    'jild25-masala-29': [204, 205],
    'jild25-masala-129': [380, 381],
}


def combine_parts(result_id, parts):
    parts = sorted(parts, key=lambda it: min(it['pages']))
    first = parts[0]
    rule = SAWAL_RULES.get(result_id)
    if rule and rule[0] == 'concat':
        sawal = ''.join((parts[i].get('tashreeh_sawal', '') or '')
                        for i in rule[1])
    elif rule and rule[0] == 'from':
        sawal = parts[rule[1]].get('tashreeh_sawal', '') or ''
    else:
        sawal = first.get('tashreeh_sawal', '') or ''
    title = first.get('title') or ''
    combined = {
        'id': result_id,
        'title': title,
        'volume_id': 37,
        'pages': sorted(set().union(*[set(p['pages']) for p in parts])),
        'start_page': min(min(p['pages']) for p in parts),
        'tashreeh_sawal': sawal,
        'tashreeh_jawab': ''.join((p.get('tashreeh_jawab', '') or '') for p in parts),
        'notes': [n for p in parts for n in (p.get('notes') or [])],
    }
    return combined


def select_parts(all_items, selectors):
    """Resolve selectors to the matching items (each used at most once)."""
    parts = []
    used = set()
    for sel in selectors:
        if sel[0] == 'id':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and id(it) not in used]
        elif sel[0] == 'id_start':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and it['start_page'] == sel[2]
                    and id(it) not in used]
        else:
            raise ValueError(f'unknown selector {sel}')
        assert hits, f'no items matched selector {sel}'
        for it in hits:
            used.add(id(it))
        parts.extend(hits)
    return parts


def run_merge(manifest_path, base, write=False):
    manifest = json.load(open(manifest_path, encoding='utf-8'))
    all_items = []
    merged_chunks = []
    for entry in manifest['chunks']:
        nn = entry['chunk']
        if entry.get('status') == 'split-halves':
            print(f'chunk {nn}: split-halves placeholder — halves are separate entries, skipping')
            continue
        # A chunk may be one file ("file") or split halves ("files").
        file_list = entry.get('files') or [entry['file']]
        items = []
        for fname in file_list:
            path = os.path.join(base, fname)
            if not os.path.exists(path):
                print(f'chunk {nn}: {fname} not yet written')
                continue
            try:
                d = json.load(open(path, encoding='utf-8'))
            except json.JSONDecodeError as e:
                # File may still be streaming from its translator; skip it
                # for now instead of crashing the whole merge.
                print(f'chunk {nn}: {fname} not valid JSON yet ({e}) — skipping for now')
                continue
            items.extend(d['masail'])
        if not items:
            print(f'chunk {nn}: no items loaded — skipping')
            continue
        # Normalize: some translators omit start_page; derive it from pages.
        for it in items:
            if 'start_page' not in it:
                assert it.get('pages'), f'chunk {nn} item {it.get("id")} has no pages'
                it['start_page'] = it['pages'][0]
                print(f'chunk {nn}: derived start_page={it["start_page"]} for {it["id"]}')
            assert it['start_page'] == min(it['pages']), \
                f'chunk {nn} item {it["id"]}: start_page != first page'
            it['_src_file'] = file_list[0]
        all_items.extend(items)
        merged_chunks.append(nn)
        entry['status'] = 'merged'
        print(f'chunk {nn}: {len(items)} items merged')
    print(f'items before combines: {len(all_items)}')
    assert len(all_items) == 191, f'expected 191 chunk items, got {len(all_items)}'
    # COMBINE the 5 cases (one mas'ala split across chunks).
    for result_id, selectors in COMBINES.items():
        parts = select_parts(all_items, selectors)
        combined = combine_parts(result_id, parts)
        assert combined['pages'] == EXPECTED_COMBINED_PAGES[result_id], \
            f'{result_id}: pages {combined["pages"]} != expected {EXPECTED_COMBINED_PAGES[result_id]}'
        exp_sawal, exp_jawab = EXPECTED_COMBINED_TEXT[result_id]
        assert len(combined['tashreeh_sawal']) == exp_sawal, \
            f'{result_id}: sawal {len(combined["tashreeh_sawal"])} chars != expected {exp_sawal}'
        assert len(combined['tashreeh_jawab']) == exp_jawab, \
            f'{result_id}: jawab {len(combined["tashreeh_jawab"])} chars != expected {exp_jawab}'
        assert combined['tashreeh_jawab'], f'{result_id}: combined jawab is empty!'
        assert combined['tashreeh_sawal'], f'{result_id}: combined sawal is empty!'
        assert combined['start_page'] == min(combined['pages']), f'{result_id}: start_page != min(pages)'
        used_ids = set(id(p) for p in parts)
        all_items = [it for it in all_items if id(it) not in used_ids]
        all_items.append(combined)
        print(f'COMBINED {result_id}: {len(parts)} parts, pages {combined["pages"][0]}-{combined["pages"][-1]} '
              f'({len(combined["pages"])} pages), sawal {len(combined["tashreeh_sawal"])} chars, '
              f'jawab {len(combined["tashreeh_jawab"])} chars, notes {len(combined["notes"])}')
    # RENAMES: none to apply as a separate step (no merge-time renames
    # in this volume; the applied-in-chunk rename is already in the
    # chunk files and is asserted present below).
    for old_id, new_id in RENAMES.items():
        assert not any(it['id'] == new_id for it in all_items), \
            f'rename target {new_id} already exists!'
        hits = [it for it in all_items if it['id'] == old_id]
        assert len(hits) == 1, f'rename source {old_id}: expected exactly 1 item, found {len(hits)}'
        hits[0]['id'] = new_id
        print(f'RENAMED {old_id} -> {new_id} (pages {hits[0]["pages"][0]}-{hits[0]["pages"][-1]})')
    # Verify absorbed ids are gone.
    for sid in ABSORBED:
        assert not any(it['id'] == sid for it in all_items), \
            f'absorbed id {sid} must not exist after combining!'
    print(f'absorbed ids gone: {len(ABSORBED)}')
    # Verify applied-in-chunk renames exist (already in the chunk files).
    for sid in RENAMED_IN_CHUNK:
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'applied-in-chunk id {sid}: expected exactly 1 item, found {len(hits)}'
    print(f'applied-in-chunk renames present: {RENAMED_IN_CHUNK}')
    # Verify BOTH masala-29 and masala-129 exist as separate items
    # with their exact pages (the Jild 24 masala-279 lesson — do NOT
    # treat 129 as a duplicate of the genuine 29).
    for sid, exp_pages in BOTH_29_AND_129.items():
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'{sid}: expected exactly 1 item, found {len(hits)}'
        assert hits[0]['pages'] == exp_pages, \
            f'{sid}: pages {hits[0]["pages"]} != expected {exp_pages}'
    print(f'both 29 and 129 present as separate items: {BOTH_29_AND_129}')
    ids = [it['id'] for it in all_items]
    assert len(ids) == len(set(ids)), f'STILL DUPLICATE IDS: {[i for i in ids if ids.count(i) > 1]}'
    empty = [it['id'] for it in all_items if not it.get('tashreeh_jawab')]
    assert set(empty) == EMPTY_JAWAB_ALLOWED, \
        f'EMPTY JAWAB mismatch: {sorted(empty)} != {sorted(EMPTY_JAWAB_ALLOWED)}'
    print(f'empty jawab (allow-listed only): {sorted(empty)}')
    empty_sawal = [it['id'] for it in all_items if not it.get('tashreeh_sawal')]
    assert set(empty_sawal) == EMPTY_SAWAL_ALLOWED, \
        f'EMPTY SAWAL mismatch: {sorted(empty_sawal)} != {sorted(EMPTY_SAWAL_ALLOWED)}'
    print(f'empty sawal (by design only): {sorted(empty_sawal)}')
    pages = set()
    for it in all_items:
        pages.update(it['pages'])
    # PRIMARY coverage check (Jild 17 lesson): validate against the 608
    # unique pages directly, not against a range-minus-gaps computation
    # (pp. 304 and 401-402 are inter-chunk gaps inside NO chunk's span).
    assert len(pages) == 608, f'expected 608 unique pages, got {len(pages)}'
    assert min(pages) == 5 and max(pages) == 658, \
        f'page span {min(pages)}-{max(pages)} != 5-658'
    # Secondary cross-check: per-chunk page count and item count must
    # equal the manifest's values for that chunk. (This manifest uses
    # 'pages' for the unique-page COUNT and 'items' for the item count;
    # combined items carry pages from several chunks, so per-chunk
    # attribution must come from the raw file, not from the merged items.)
    for entry in manifest['chunks']:
        if entry['chunk'] in merged_chunks:
            d = json.load(open(os.path.join(base, entry['file']), encoding='utf-8'))
            raw_pages = set()
            for it in d['masail']:
                raw_pages.update(it['pages'])
            assert len(raw_pages) == entry['pages'], \
                f'chunk {entry["chunk"]}: {len(raw_pages)} unique pages != manifest {entry["pages"]}'
            assert len(d['masail']) == entry['items'], \
                f'chunk {entry["chunk"]}: {len(d["masail"])} items != manifest {entry["items"]}'
    print(f'total items: {len(all_items)} | pages covered: {len(pages)}')
    assert len(all_items) == 168, f'expected 168 items after combines, got {len(all_items)}'
    # sort by start_page for the final file
    all_items.sort(key=lambda it: it['start_page'])
    for it in all_items:
        it.pop('_src_file', None)
    if write:
        with open(os.path.join(base, 'jild-25.json'), 'w', encoding='utf-8') as f:
            json.dump({'masail': all_items}, f, ensure_ascii=False, indent=1)
        with open(os.path.join(base, 'chunks-manifest-jild25.json'), 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f'WROTE jild-25.json: {len(all_items)} items, {len(pages)} pages, chunks merged: {merged_chunks}')
    return all_items, pages, merged_chunks


def main():
    manifest_path = os.path.join(BASE, 'chunks-manifest-jild25.json')
    run_merge(manifest_path, BASE, write=True)


if __name__ == '__main__':
    main()
