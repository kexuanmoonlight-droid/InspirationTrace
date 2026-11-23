# V5.1 — Manual acceptance test (Offline Demo)

> This is a **scripted, non-generative prototype**. Its cards contain actual public book-page URLs manually curated from publisher or publisher-distribution pages, not AI-retrieved live results. An official page corroborates a book's identity/description, **not** a measured story similarity, originality score, plagiarism, or any influence on an LLM.

## Reset and run

1. Stop previous PowerShell server with `Ctrl+C`.
2. Extract the **entire** V5.1 ZIP into a new folder containing `server.py`.
3. In that folder, run `py server.py` and visit `http://127.0.0.1:8765/`.
4. Select **离线脚本演示（免费，无AI）**. Browser data is stored separately from V5.0, so older drafts will not appear. Export old drafts from V5.0 if needed.
5. Keep **更新大纲后更新右侧材料** checked.

## Three-round walkthrough (fantasy is an EXAMPLE, not a genre restriction)

| Test | Exact interaction | Expected observation |
|---|---|---|
| F01 | Click **加载奇幻救援示例**, then **发送并继续创作** | V1 outline displayed; right sidebar shows 2 **manually curated real-book links**; V1 now underlines **王室曾经的背叛** and **救出被困山谷的王子** as **broad, limited thematic comparisons**, not dragon or textual matches |
| F02 | Type **加入龙元素**, send | V2 updates across plot sections; prior V1 selectable; right sidebar links section(s) to candidate book cards |
| F03 | Type **我想让龙和王子产生多一些的关系**, send | V3 appears; prince/dragon/princess relationships alter motivations, conflict and ending; V1/V2 remain available |
| F04 | Click a blue-underlined V3 story section | Related card on right highlights; clicking a card highlights the related outline section |
| F05 | Click **打开真实作品页面** on each fantasy card | Opens the matching publisher/publisher-distribution product page in new tab |
| F06 | Tick **加入参考**, **标记已审阅** for one work | States remain on the selected version; neither action claims verification of originality |
| F07 | Click **重新检索** | Loads the **same manually curated evidence**; review/selection flags for matching records are retained. No online search occurs |
| F08 | Select V1 then click **恢复版本**; later select V3 and restore | Shows relevant outline and evidence state for selected version |
| F09 | Send unsupported instruction **把地面换成积木** | Explicit limitation message; no invented V4 outline |
| F10 | View API error history in `TEST_REPORT.md` | HTTP 429 OpenAI generation remains Blocked; offline success does NOT clear that block |

## Book evidence records

1. Samantha Shannon, *The Priory of the Orange Tree*, Bloomsbury Publishing: https://www.bloomsbury.com/uk/priory-of-the-orange-tree-9781408883358/ — dragons, political conflict; **thematic** comparison only.
2. J. R. R. Tolkien, *The Hobbit*, HarperReach/HarperCollins: https://www.harperreach.com/products/the-hobbit-j-r-r-tolkien-9780007458424/ — dragon/adventure, **weak and broad** motif comparison only.
3. For the separate memory-case example, *The Memory Police* is a pre-existing V5 sample. Its publisher URL should be manually checked as part of user acceptance before publication.

Record results in Excel as `Offline / Scripted` with screenshot and exact observed result. User-run browser tests above are **pending**, not automatic passes. For a clean run, use an InPrivate window or clear only this site's browser storage after exporting any needed drafts.

## V5.2 required hover regression test (do not omit)

1. Select **离线脚本演示**; load **奇幻救援示例** and send. Both source cards should exist, and V1 should underline **王室曾经的背叛** (Priory: broad politics) and **救出被困山谷的王子** (Hobbit: broad adventure). These do not imply V1 has dragon content.
2. Enter `加入龙元素` to make V2. Underlined phrases should be visible in the current outline. Hover **王国试图夺取龙焰控制山区资源**: *The Priory of the Orange Tree* record in the right sidebar should light up. Hover **沉睡的古龙已经苏醒**: *The Hobbit* record should light up.
3. Move pointer away: highlight clears. Hover either source card: the corresponding outline phrase/section should highlight in reverse. Test keyboard Tab focus if practical.
4. Enter `我想让龙和王子产生多一些的关系` to make V3. Hover **龙族担心人类再次背约** and **公主深入灰烬山脉寻找王子** and check corresponding separate cards.
5. Confirm both source links open the corresponding real publisher/distributor pages, then test **加入参考**, **标记已审阅** and version restore. Record actual findings and screenshots; **do not pre-fill Pass**.

## V5.4 regression fix — observed V1 missing underline (must retest on student's Windows)

The student supplied a screenshot showing **V1** with two source cards but **zero underlined phrases**. Inspection found that the offline evidence generator intentionally returned `sectionIndex=None` and empty `highlightText` for V1, so previous V5.2/V5.3 assertions about “restored hover” did not cover V1. This was an implementation mismatch with the original fixed design requirement, not a browser refresh issue.

1. Confirm the page header says **V5.4** (to rule out an old server).
2. In offline demo, load fantasy V1. Underline anchors: **王室曾经的背叛** → *The Priory of the Orange Tree*, and **救出被困山谷的王子** → *The Hobbit*. These are **broad thematic prompts** only; do not assert dragons in V1 or verified textual overlap.
3. Hover each underline individually; only its corresponding right card should light up. Hover the card to verify reverse emphasis; move away to clear.
4. Repeat with V2 and V3, then restore V1. Confirm the links/checkboxes and version state still work.
5. Log a screenshot for V1 underlining + hover. Record **student browser acceptance pending** until actually checked.


## Acceptance update (23 November 2026)

The student subsequently reported that the **full V5.4 workflow and project export were successful, with no issues observed**. Treat the walkthrough as student-reported Pass at the summary level. Screenshots and granular F01–F10 observations should be retained separately if they exist; do not fabricate missing individual evidence or treat the demo as real AI generation.
