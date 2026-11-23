# InspirationTrace — Design Decisions, Development and Review Log

**Project:** InspirationTrace (A1-informed A2 intelligent-interaction prototype)  
**Record type:** Retrospective reconstruction from the project conversation and supplied artefacts, prepared 2026-11-23; this is not a contemporaneous V1–V4 Git history.  
**Important distinction:** A **student observation/decision** records a stated judgement or reported interaction. A **developer change** records a generated or proposed implementation. A **test result** requires an identifiable executed check. Discussion alone is not a passed test.

## A. Research continuity and decisions

| ID | Stage | Student's input or observation | Design decision and reason | Evidence status |
|---|---|---|---|---|
| R01 | A1 → A2 research scope | Originality and resemblance are the concern for online novel authors; AI can already assist ideation. | Focus A2 on inspectable evidence during creative expansion, not claiming that the system proves originality. | Documented student decision; not a user-study finding. |
| R02 | A1 literature alignment | Keep A1 citations and constraints; Wang et al. (2025) concerns visual designers rather than novelists. | Retain appropriate A1 evidence with its participant/population limitation; later restore omitted Wang citation. | Document editing/review, not system test. |
| R03 | Idea-first workflow | Novelists develop from one seed/fragment rather than needing numerous separate reference cards. | Replace reference-card-first interaction with a coherent, generated story outline. | Student's rationale; requires user validation before generalising. |
| R04 | Scope of narrative | The author may build people, world, conflict or alternate plot trajectories. | Do not hard-code genre, character count or a princess/dragon story as the general model. | Student decision; open-ended generation not yet validated. |
| R05 | Evidence in creative workflow | Originality assessment is difficult because origins and similar works are not clearly inspectable. | Right sidebar separates traceable records from candidate similar works, with real links when available. | Design decision; link relevance/coverage requires checking. |
| R06 | Author agency | Author controls whether to use ideas and references. | Right panel only adds/removes chosen references and marks review; creative input and regeneration decisions remain with author. | Interface requirement; not proof of improved originality judgement. |
| R07 | Linked interaction | Author should inspect evidence without leaving the story. | Underlined passages focus/highlight the matching sidebar card; reverse navigation is target behaviour. | UI implementation varies by version; current matching is section-level. |
| R08 | Split layout | Top left: outline; bottom left: conversational author input; right: evidence. | Establish one split workspace inspired by document-plus-sidebar pattern. | Confirmed interface design. |
| R09 | Cyclic storyboard | After evidence review, the author returns to input and iterates until satisfied. | Explicit human-controlled loop, with recoverable outline versions. | Confirmed target storyboard; individual feature testing separate. |
| R10 | Free conversation | Continuous conversation should not force new-outline generation on every turn. | Separate conversation-only turns from regenerate-outline commands. | V4 cloud mode designed for this; live behaviour not verified due to quota. |
| R11 | Provenance boundary | A similar novel found after generation is not necessarily a source consulted by the model. | Label retrieved works as candidates; never equate search links with model provenance, citation certainty, plagiarism or a positive originality verdict. | Design safeguard; automated accuracy unverified. |

## B. Software iterations and actual feedback

| ID | Version / change | Student-discovered issue or request | Implemented or proposed response | Verification and boundary |
|---|---|---|---|---|
| D01 | Initial HTML editor | Initial artefact was an element-based walkthrough with prepared content. | Manual add/edit/delete, undo, review state, local version history and JSON export. | Earlier developer-described local checks; **not** equivalent to the later V4/V5 tested workflow. |
| D02 | V1 / first revised prototype | Story-first, side evidence and cyclic experience requested. | Static demonstration outlines, sidebar and version actions. | Interaction implementation existed; true AI ideation was absent. |
| D03 | V2 conversation fix | Second-round input did not meaningfully change an existing outline; user reported that the chat felt stuck. | Visible conversation records and saving submitted instructions into another outline version. | Developer simulation was reported; merely appending instructions did **not** meet open-ended creative continuity. |
| D04 | V3 live-generation design | User explicitly rejected simple addition of the next instruction to a fixed outline. | Build an API-backed path that passes current outline plus previous exchanges to a generative model. | Mock integration described in development; not proven with a live model. |
| D05 | Genre neutrality | Princess-rescues-prince and dragon were **illustrative user examples**, not product requirements. | Remove scenario-specific framing from general task specification; open creative input should support any genre. | Confirmed user correction; open-ended quality not yet tested. |
| D06 | V4 baseline | User finalised free-form multi-turn chat, separate evidence sidebar with genuine links, and source selection. | Python-backed dialogue, outline version flow, candidate search endpoint, UI evidence and link controls. | Five mock-contract tests; live AI and retrieval not yet validated. |
| D07 | Test planning | User asked what coursework requires, how many cases and how to record them. | Prepare a 12-case Excel test log, use formal `TEST_REPORT.md`, retain screenshots and `Blocked` states. | Test-planning artefact, not 12 completed manual tests. |
| D08 | Student Windows setup | `python --version` gave no version; `py --version` initially not recognised. | Install Python and retry in correct extracted project directory. | Student later showed `Python 3.14.10`; environment prerequisite passed. |
| D09 | Student backend test | User ran `py test_backend.py` in the V4 directory. | No code change required at this point. | **Student screenshot:** `Ran 5 tests ... OK`; 5/5 V4 mock tests passed on user's Windows machine. |
| D10 | API setup | User created an active API key and configured the PowerShell environment variable. | Server uses environment variable rather than embedding credentials in source. | Student showed `API Key configured` and a running V4 service on `http://127.0.0.1:8765/`; this is **not** proof of valid billing or live-generation success. |
| D11 | Billing-blocked live generation | On a fresh story prompt, site reported HTTP **429**, `insufficient_quota` / `credit_balance_exhausted`. | Mark first live-generation case **Blocked**; preserve draft/input; advise not to count it as generated output. | **Student screenshot:** true HTTP error observed; no outline generated. Payment attempt later failed, so no successful live cloud call can be claimed. |
| D12 | OpenAI payment barrier | User reported that a mainland-issued card was rejected and available alternative funds were insufficient. | Avoid making paid cloud API a hard prerequisite for A2 deliverable. | Student-reported payment constraints; no payment diagnostics beyond 429 should be invented. |
| D13 | V5 offline / local revision | User approved a free demonstrable fallback with a potential local model. | Add three selectable modes: Offline scripted demo (default), Ollama adapter (optional), OpenAI cloud (preserved). | 7 additional offline unit tests passed in developer environment; user has **not yet shown** V5 Windows/browser tests. |
| D14 | Offline honesty | A scripted story must not be mistaken for genuinely understanding any user's prose. | Supported fixed scenarios only; unsupported prompts explicitly reveal simulation; source comparison is manually curated. | Implementation/automated-test claim; cannot claim open-ended generation from scripted mode. |
| D15 | Local model possibility | Real multi-turn inference without usage-based cloud billing may be possible with Ollama. | Provide an adapter and setup guidance; do not auto-download/install model. | No user device capability or live Ollama inference verified. |

## C. Coursework and report edits (NOT application test outcomes)

These are documented writing and submission changes, not evidence that software functionality works:

1. Repeated alignment of A2 problem, abstract and rationale with A1 originality-assessment question; narrowed to online novel authors.
2. Replaced linear Adopt/Revise/Reject-oriented card storyboard with document-centred cycle and clear author-controlled continuation.
3. Redrew Architecture to distinguish intended source retrieval, context assembly, source-to-passage mapping and versions.
4. Retained A1's nuance: Doshi and Hauser concern collective diversity, not proof of plagiarism; Wang concerns visual designers rather than novelists.
5. Student flagged omission of Wang et al. (2025) during a V4 report update; the citation and reference were restored.
6. References subsequently aligned to A1's APA style and to cited A2 sources; citations must not be silently removed in future technical edits.
7. Updated A2 to distinguish the implemented V5.5 scripted demo from the unverified live-model and dynamic-retrieval paths. The final report links a specific repository commit; it must be updated if the submission snapshot changes.

## D. Evidence inventory and verification limits

| Evidence ID | Available evidence in conversation / project | Claim it can support | Not supported |
|---|---|---|---|
| E01 | Windows PowerShell screenshot: `Python 3.14.10` | Python available to student | Application works end to end |
| E02 | Windows PowerShell screenshot: `Ran 5 tests ... OK` | 5 V4 mock tests executed by student | True AI quality or source retrieval |
| E03 | Windows PowerShell screenshot: `API Key configured` and V4 startup on port 8765 | Environment variable set and local service started | Successful cloud inference |
| E04 | V4 UI screenshot with HTTP 429 and preserved input | Live model request blocked by exhausted API credit; UI preserved the typed text in this observed case | Success of initial outline generation |
| E05 | Developer-run V5 12 unit tests and smoke check | Automated scripted-mode/backend checks in development environment | Student browser testing or local Ollama quality |
| E06 | Approved cyclic storyboard and recorded chat feedback | User-defined design requirements and author-involved corrections | Quantified user-study findings |
| E07 | [Chinese V5.4 JSON export](evidence/V5_4_Chinese_scripted_test_export.json) | Three scripted outline versions, six chat messages and version-specific thematic reference states | English V5.5 output, live model generation or source-retrieval quality |
| E08 | [V5.5 student and mocked-browser screenshots](screenshots/) | Browser presentation and interface controls, with tester provenance identified in `TEST_REPORT.md` | Real-author effectiveness or unscripted model capability |

**Screenshot hygiene:** A previous PowerShell screenshot displayed a long API-key fragment. Do **not** upload raw terminal screenshots containing credentials to a public GitHub repository. Redact all key fragments and personal paths where desired, or create a safe text-only reproduction of the error code. If full credentials could have leaked, rotate the key.

## E. Lessons and verification boundary

The student rejected appending new prompt text to a fixed story as a substitute for coherent co-creation. This led to an outline-and-conversation context design and, when cloud access was blocked, to an openly scripted prototype. The student verified V4 mocked tests and the HTTP 429 incident, then identified subsequent scripted third-turn and highlighting defects. V5.4 and V5.5 browser acceptance is recorded separately from automated regression checks. **No live open-ended generation or automatic similarity retrieval has been validated.**

**Git provenance:** all public repository commits were made on 23 November 2026, when earlier local work was uploaded. This log reconstructs earlier decisions retrospectively from the conversation, uploaded documents and available artefacts; it is not a substitute for time-stamped intermediate Git commits. Commit dates have not been altered or backdated.

## Follow-up observation: scripted third turn and empty evidence sidebar (23 November 2026)

The project author reported that the first two outline stages appeared, but a third creative instruction concerning character relationships did not produce an updated outline. They also observed no displayed references or similar works in the right sidebar. Examination of `offline_modes.py` confirmed fixed follow-up scripts and a source example limited to the memory-trading scenario. This supports diagnosing the *offline mode's known scope*; this observation was later addressed with a bounded V5.1 scripted demonstration, not a live-model fix.

**Student feedback:** This does not meet the confirmed goal of natural, open-ended multi-turn creative co-writing with dynamically retrieved evidence.

**Design consequence:** Retain transparent scripted mode for testing the interface, but prioritise testing a real local generation model (subject to device capability). A distinct verified retrieval strategy remains necessary for live similar-work results.

**Verification boundary:** No claim that the third turn was handled by a real model or that dynamic provenance retrieval was tested. See TEST_REPORT.md OBS-V5-001 and OBS-V5-002.


## 2026-11-23 — V5.1 targeted repair (AI-assisted)

Student requested that the existing V5 small interaction loop be repaired rather than rewriting the A2 report/storyboard before testing. Specifically, a third-round change to prince/dragon relationships and credible **real URLs** for right-sidebar candidate published works were required. An AI-assisted change supplied one transparent predetermined V3 branch, two manually verified published-work pages, source-to-outline association, persistent review selections on refresh, and test documentation. This supports a bounded demonstration, not conversational understanding or dynamic source similarity. Automated tests passed (14/14); later acceptance relates to V5.4 and V5.5 after additional hover fixes.

## V5.2 — Restoring an original interaction requirement

**Student-reported concern:** During V5.1 testing, the requested underlined passage and hover-to-highlight correspondence with the right citation panel seemed to have disappeared. Student explicitly required that original design constraints must not be silently removed in subsequent iterations.

**Decision:** Treat the linkage as a non-negotiable requirement; correct it in place rather than changing layout or dropping other V5.1 functionality. An implementation bug was identified: entire-section underlining with only the first candidate selected, combined with no anchor on the first fantasy stage, did not deliver predictable phrase-to-card highlighting.

**AI-assisted change:** Add exact phrase anchors in evidence data, bidirectional pointer/keyboard highlighting, visible-scroll behavior, and regression tests. Keep real-source links and caution against treating thematic overlap as evidence of copying.

**Verification at V5.2:** Automated tests and JS syntax checks passed, but subsequent student testing revealed V1 annotations were still missing. The issue was fixed later in V5.4.


## V5.4 — Student visual regression exposed missing V1 anchors

The student supplied a V1 screenshot showing actual candidate source cards but no underlined spans, after reporting that refreshing did not help. We inspected the source and found that this was by design in the earlier scripted stage-1 evidence mapping, in contradiction to the student's original hover-link specification. The earlier V5.2 and V5.3 changes were insufficient: their regression tests covered hover handlers but explicitly allowed V1 to have no anchor. The developer therefore made a narrowly scoped change to stage-1 evidence mapping and browser migration, preserved all other behavior, and added a unit test and Chromium DOM smoke test. The new V1 labels are broad thematic pointers, not source attribution, text overlap, or plagiarism proof. The student subsequently verified the corrected behaviour on Windows as part of the full V5.4 walkthrough.


## 2026-11-23 — Student accepts V5.4 and chooses to move to submission preparation

The student reported completing the full V5.4 workflow and a successful project export with no observed problems. This follows their earlier detection of the missing V1 underline-to-evidence hover interaction and the targeted fix. The development decision is to stop adding prototype features, retain V5.4 as the **accepted offline scripted demonstration**, and next prepare GitHub evidence and align the written A2 artefacts. This acceptance does **not** verify dynamic retrieval or live free-form AI generation, which remain constrained by API availability or untested local inference. No earlier Git commits should be invented or backdated.


## 23 November 2026 — V5.5 English-language interface (AI-assisted, user-requested)

After the student confirmed the V5.4 offline interaction and JSON export, the student supplied two Windows screenshots and requested English-language presentation for the final coursework, including updating GitHub. The implementation retained the entire interaction model and backed up the accepted Chinese sources under `legacy_zh/`. Labels, three scripted example scenarios, scripted conversation responses, English evidence comparisons, and V1–V3 phrase-level hover anchors were translated. Student V5.4 screenshots remain historical evidence; V5.5 was checked with 19 Python tests and a mocked-API headless browser smoke test, and subsequent independent student acceptance on Windows was reported after this build. No change was made to the intended study population or open-ended AI co-creation ambition; cloud API billing remains blocked.


## 23 November 2026 — student acceptance of final English prototype

Following the English localisation and automated regression checks, the student independently reported completing all V5.5 English browser tests successfully, with no observed issues, and provided additional screenshots for final coursework preparation. The accepted scope remains the transparently scripted three-round creative/review interaction, version restore, linked thematic cards and export. Open-ended generative AI and automated source retrieval remain unverified due to the earlier API credit constraint. Coursework report and storyboard were then aligned with this accepted implementation.
