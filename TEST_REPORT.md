# InspirationTrace V5 — Test Report

**Record updated:** 2026-11-23  
**Testing basis:** V4 cloud implementation retained; V5 adds offline scripted demo and optional Ollama adapter.  
**Full design change history:** [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md)  
**Hands-on offline steps:** [OFFLINE_TEST_STEPS.md](OFFLINE_TEST_STEPS.md)

## 1. Executed checks — identify the tester and environment

| Test group | Environment / tester | Result | Evidence and scope |
|---|---|---|---|
| V4 mocked backend tests | **Student, Windows PowerShell** (`py test_backend.py`) | **PASS 5/5** | Student-supplied terminal screenshot: `Ran 5 tests ... OK`; mock contracts only |
| Python installation prerequisite | **Student, Windows** | **PASS** | `py --version` showed Python 3.14.10 |
| V4 startup | **Student, Windows** (`py server.py`) | **PASS: server started** | Local address `http://127.0.0.1:8765/` printed; does not imply API works |
| API key environment check | **Student, PowerShell** | **PASS: variable present** | `API Key configured`; no secret value retained here |
| V4 live outline generation | **Student, browser** | **BLOCKED — HTTP 429** | Model response `insufficient_quota`, `credit_balance_exhausted`; no outline returned |
| V4 error handling on this attempt | **Student, browser** | **OBSERVED: input retained** | Site displayed error and retained typed input/draft; one-case observation, not full recovery test |
| V4 5 mocked contract tests, V5 7 offline tests | **AI-assisted development environment** | **PASS 12/12** | `python -m unittest test_backend_v4.py test_offline_modes.py`; tests cover mocked and scripted logic only |
| Python syntax / embedded JavaScript syntax | **AI-assisted development environment** | **PASS** | Compilation / syntax checks; not UI usability verification |
| Local HTTP smoke (offline endpoints) | **AI-assisted development environment** | **PASS** | `/api/chat` and `/api/status` worked without a key in scripted mode |
| V5 Windows browser end-to-end | **Student** | **NOT TESTED** | Awaiting personal test |
| Ollama real local inference | **Student** | **NOT TESTED** | Model not installed/verified in this record |
| Real similarity retrieval accuracy | **Student** | **NOT TESTED** | No validated end-to-end search; curated demo link is not search evidence |

**Interpretation:** The observed HTTP 429 is an **external billing blocker**, not evidence of incorrect story-generation semantics. Likewise, the 12 green developer-side tests do **not** prove the user's computer can run V5 or that a real model produces coherent stories.

## 2. Incident record: V4 API credit exhaustion

- **Incident:** INC-API-001
- **Related manual case:** T01 — initial story generation
- **Prerequisites observed:** Python installed; V4 mock tests passed; environment variable configured; local server listening.
- **Student input:** Requested a fantasy story about a strong princess rescuing a prince (a *test example*, not a genre restriction).
- **Expected:** A fresh, coherent story outline and optionally candidate-work search results.
- **Actual:** Web page displayed `Model service HTTP 429`, `insufficient_quota`, `credit_balance_exhausted`, and a provider message indicating zero available API credit. No new generated outline.
- **Input handling:** The UI reported that the entered idea and draft were retained; they were visible in the supplied screenshot.
- **Classification:** **Blocked / external API billing**, rather than Pass or Fail for creative generation.
- **Action/decision:** The student reported unsuccessful card payment and insufficient alternate balance, approved a non-billing fallback; V5 added a clearly labelled offline scripted demo and an optional unverified Ollama adapter. Existing cloud mode was preserved.
- **Retest:** A successful live OpenAI generation has **not** been demonstrated. Offline scripted testing is a **different test**, not a retest that resolves T01's live-AI block.
- **Security:** Never paste or upload an API key or unredacted terminal screenshot to the repository.

## 3. Manual test statuses: V4 plan and V5 offline alternative

### Original V4 T01–T12 (live/intelligent functionality)

| ID | Status as of this record | Notes |
|---|---|---|
| T01 initial real-model story generation | **Blocked** | HTTP 429 in student's browser |
| T02 multi-turn semantic integration | Not tested live | Earlier user feedback on fixed/scripted versions must not be counted as a V4 live pass |
| T03 ordinary chat without updating outline | Not tested live | API-based dialogue not validated by student |
| T04 major change of narrative direction | Not tested live | |
| T05 automatic candidate-work retrieval | Not tested live | |
| T06 real URL/content verification | Not tested systematically | Curated publisher link exists as example; relevance requires manual inspection |
| T07 underline → matching sidebar feedback | Not tested by student on V5 | Section-level mapping only |
| T08 add/remove reference | Not tested by student on V5 | |
| T09 reviewed/unreviewed | Not tested by student on V5 | |
| T10 restore outline version | Not tested by student on V5 | |
| T11 branch from historical version | Not tested | Shared conversation history may bleed between branches |
| T12 API failure and recovery | **Partially observed** | HTTP 429 visible; input retained in that observed instance; other failures untested |

### V5 offline scripted demo: separate acceptance track

Follow [OFFLINE_TEST_STEPS.md](OFFLINE_TEST_STEPS.md) for D01–D08. The developer-side offline automated tests pass; the student's Windows browser results are **Pending** for all D01–D08. When running them, record actual outputs, browser version, date, and evidence filenames. The demo is **simulated**, never a live substitute for T01/T02/T05.

| Demo | Intended check | Student result |
|---|---|---|
| D01 | Offline server and default mode without cloud key | Not tested |
| D02 | Load and present prepared outline V1 | Not tested |
| D03 | Supported scripted revision and version creation | Not tested |
| D04 | Restore V1 | Not tested |
| D05 | Curated link to existing work; no auto-search claim | Not tested |
| D06 | Click underlined section to focus evidence | Not tested |
| D07 | Add/remove and reviewed/unreviewed controls | Not tested |
| D08 | Honest unsupported-prompt fallback | Not tested |

## 4. Development issues, decisions and verification trail

| Ref | Concern | Student decision | Change status | Verification boundary |
|---|---|---|---|---|
| UX-01 | Detached suggestion cards disrupt an idea-first creative flow | Outline above free-form conversation, sources in sidebar | Confirmed design and prototyped across versions | No user study proving superiority |
| UX-02 | Earlier demo ignored or appended second-round instructions | Reject pseudo-AI string appending; carry current outline and history into live model call | V3/V4 architecture written | Real model continuity untested |
| UX-03 | Example with princess/prince/dragon was mistaken for product scope | Do not restrict genres or story structure | Generalised generation specification in live path | Only scripted demo contains fixed stories |
| UX-04 | Evidence source potentially confused with model provenance | Label similar works as candidates; keep selection distinct from evidence records | UI and README safeguards | Automatic attribution accuracy untested |
| UX-05 | Limited API credit makes mandatory cloud calls untestable | Preserve cloud code; add honest offline demo and optional local model | V5 development branch | New demo needs student browser verification |

Further context and A1/A2 report corrections are recorded in [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md).

## 5. Known limitations and ethical reporting

- Offline script cannot understand arbitrary ideas; unsupported prompts must not receive fabricated 'AI' output.
- Ollama integration is adapter code, not demonstrated local inference.
- Candidate search may find works related in theme; a source URL alone does not prove narrative overlap, plagiarism, completeness or model provenance.
- Evidence underlines currently refer to **outline sections**, not validated quoted substrings.
- Browser local state and a shared conversation history can complicate branching and restored-version context.
- No user study has shown that InspirationTrace improves originality judgement.
- Screenshots for a public repository must have all secret-key fragments removed.

## 6. Manual testing instructions and reporting format

Use the existing Excel workbook for full inputs and outputs. Summarise here only the actual result, issue ID, fix (if any), and retest. Use **Pass**, **Fail**, **Partial**, **Blocked**, **Simulated**, or **Not tested** accurately. Record observed result first; write suspected causes separately.

Suggested issue row:

`Issue ID | build/mode | steps and input | expected | observed | severity | student decision | AI-assisted change | retest result | screenshot filename`

**Before final submission:** finish D01–D08, choose whether to test a live local model, update GitHub commit and README, and revise A2's delivery/validation claims to match the actual submitted version.


## 7. New student-reported V5 observations (23 November 2026; pending independent retest)

These are **author-reported observations**, not automated test passes or evidence of a live model failure. The precise selected mode and input wording were not separately captured; behaviour matches the Offline Demo branch on code inspection.

| Issue | Student observation | Code-supported diagnosis | Classification | Retest |
|---|---|---|---|---|
| OBS-V5-001 | After two outline rounds, a third request to add relationships among characters produced no new outline or apparent response | `offline_modes.py:mock_chat` implements only limited fixed next-step scripts. For a fantasy example, it handles a dragon addition at stage 1; unmatched subsequent edits return `updated:false` with a limitation message. The UI does not create a new outline on that response | Offline scripted capability limit; not a proven live-LLM defect | Reproduce in browser with mode shown; check conversation feedback and unchanged outline |
| OBS-V5-002 | Evidence sidebar displayed no source or similar-work records during the multi-round scenario | `offline_modes.py:demo_evidence` has a curated publisher-linked comparison only for `memory`; `fantasy` and `mystery` return empty records. Offline demo does not run live search | Missing scripted data / no dynamic retrieval in Offline Demo | Run memory example (D05-D07) to inspect prepared record; test dynamic retrieval only after a live provider is available |

**Development response:** Do not expand the handful of fixed narratives and misrepresent them as open-ended AI. Keep the mock mode for inspectable UI and recovery checks; investigate optional local Ollama for genuine free-form generation. Dynamic similar-work search remains separate and is not provided merely by installing Ollama.

**Recording note:** In the Excel log, mark the unsupported third-round creative request as `Blocked / Not supported in Offline Demo`, not a failed real AI reasoning test. Mark the absent records as `Not available in this offline scenario`, not a source verification success.


## V5.1 changes and test status (2026-11-23)

The student observed that the fantasy demo stopped at a third-round character-relationship request and showed no related-source cards. V5.1 addresses these with a **fixed third scripted revision** and two **manually curated, publicly verifiable book pages** (Bloomsbury / HarperReach). Automated testing: **14/14 pass** (V4 regression: 5; original V5: 7; V5.1 additions: 2). JavaScript syntax: pass. **Student-run browser acceptance F01–F10: Pending**. This does **not** clear the previously recorded cloud API T01 HTTP 429/insufficient-credits blocker, nor prove real LLM generation or live similarity search. See `OFFLINE_TEST_STEPS.md` and `V5_1_CHANGELOG.md`.

## V5.2 regression issue — inline underline / sidebar hover link

**OBS-V5-003 — Reported by student:** V5.1 appeared to lose the original requirement: underline the corresponding story phrase and highlight its linked source card in the right panel on mouse hover. The V5.1 implementation retained partial hover code but lacked exact phrase anchors and reliable card visibility. **V5.2 corrected** the phrase-level mapping, two-way hover/focus behavior, and scroll-to-card. Also preserved manual-source, non-plagiarism disclosures.

**Automated result:** original 14 Python tests + 3 dedicated regression tests passed. JavaScript syntax verified. **Manual browser validation: PENDING.** No claim that the student has already seen or accepted the repaired interaction.

**Reproduction / student retest:** In V5.2, load fantasy demo → send → `加入龙元素` → hover the underlined phrase `王国试图夺取龙焰控制山区资源`; the *The Priory of the Orange Tree* card should highlight. Hover `沉睡的古龙已经苏醒`; the *The Hobbit* card should highlight. Then send `我想让龙和王子产生多一些的关系` and repeat with `龙族担心人类再次背约` and `公主深入灰烬山脉寻找王子`. Move the pointer away: transient highlights should clear. Hover each card to check reverse highlighting. Click source links to check actual pages. The initial fantasy version intentionally has no linked underline because it has no dragon-themed matching passage.


## V5.3 narrow hover-link fix (browser acceptance pending)

An additional regression path was identified: evidence cards saved by previous localStorage versions can lack `highlightText`, preventing underlines even after installing newer code. V5.3 automatically refreshes offline annotation metadata for the current demo version on startup, mode change, or restoring a saved version, while preserving the `selected`/`reviewed` flags. The original bidirectional mouse-hover linkage is unchanged. Automated code checks are not a substitute for a browser hover test.


## V5.4 — V1 underlines absent (student-confirmed) and targeted correction

- **Observed issue (confirmed by student screenshot):** fantasy V1 shows two candidate work cards, but no outline underlines and therefore no hover linkage. Hard refresh did not help.
- **Root cause (code inspected):** `demo_evidence()` intentionally had no V1 phrase mapping, returning null section indices and blank highlight text. Earlier automated tests actually **asserted that absence**, so their PASS result failed to protect the original UI requirement.
- **Small fix:** map two exact V1 phrases to *very broad thematic* candidate cards; revise comparison text to avoid implying any dragon claim in V1 or measured similarity; include V1 in saved-metadata refresh path. V2/V3 mapping preserved.
- **Automated evidence:** 19 Python unit checks passed including a new V1 anchor test; JS syntax passed. Separate Chromium DOM smoke check (with the UI's actual HTML/JS and generated V1 data injected, not a full HTTP end-to-end test) observed two underlines; left hover highlighted one corresponding right card; right hover highlighted one corresponding left anchor.
- **Student browser test:** pending. Re-test actual running V5.4 locally before marking complete.
- **API credit HTTP 429:** unchanged; still blocked. This fix does not add AI generation or live retrieval.


## V5.4 — Student-reported end-to-end browser acceptance (23 November 2026)

**Student report:** The project author confirmed that the complete V5.4 demonstration workflow was tested successfully, file export succeeded, and no problems were observed. This supersedes the previous pending-browser-check note **for the walkthrough the author actually completed**. It is evidence of student-reported acceptance, not an independently observed screen recording or proof of unrestricted AI behavior.

| Acceptance item | Recorded status | Evidence boundary |
|---|---|---|
| V5.4 scripted story and revisions | Pass — student-reported full-flow test | Exact per-step screenshots/results not supplied in this message |
| Linked underlined outline text and source-card highlighting | Pass — student-reported full-flow test following the targeted fix | Exact hover screenshots not supplied in this message |
| Source-card review, browsing and version actions | Pass — student-reported full-flow test | Whether each external URL was opened is not individually itemised |
| Project export | **Pass — explicitly confirmed by student** | Exported file contents not independently inspected |
| OpenAI live generation and dynamic retrieval | **Blocked / unverified** | Prior HTTP 429 insufficient API credits remains unresolved |
| Unrestricted conversation via local Ollama | **Not tested** | Local model not confirmed installed or run |

**Disposition:** Freeze V5.4 as the accepted scripted prototype. Do not interpret the earlier scripted-demo success as evidence of an operational open-ended AI model, automated similarity measurement, or provenance of model training sources. Future work is GitHub packaging, actual commit provenance and aligning the A2 report/storyboard/architecture to this accepted build.


## V5.5 EN — language-localisation regression (23 November 2026)

- **Change:** translated UI, predefined outlines, scripted responses, evidence descriptions and exact phrase anchors into English without changing feature scope. Kept `legacy_zh/` as the accepted V5.4 baseline.
- **Automated tests:** 19/19 passed in the developer environment after updating language assertions; JS syntax validation passed.
- **Browser smoke:** headless Chromium with intercepted API calls verified English fantasy V1 → V2 → V3, two underlined phrases and two source cards per stage, left-to-right and right-to-left hover highlighting, and a source review checkbox. This is a **mocked browser integration check**, not real Windows/browser acceptance or live AI testing.
- **Student Windows acceptance of the English interface:** PENDING, should be re-tested.
- **Earlier V5.4 student acceptance:** already reported by the student; two provided screenshots document the Chinese version's V3, hover focus and conversation panel.
- **Provider billing:** the observed cloud API HTTP 429 credit balance exhausted remains a blocked live-generation case; neither English translation nor offline simulation fixes API credits.
