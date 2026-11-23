# InspirationTrace — A2 Prototype (V5.5 English)

**README prose word count: 579 words** (excluding code blocks and URLs).

**Status:** Student-tested, **scripted offline interaction prototype** for online novel authors. It demonstrates three prepared story-outline turns, version recovery, linked underline ↔ evidence-card highlighting, reference/review controls and JSON export. The intended open-ended AI dialogue and automatic similar-work retrieval are **not validated**. Candidate book links are manually curated thematic comparisons—not plagiarism findings, model-used sources or originality scores.

## Technology and run instructions

- **Stack:** HTML/CSS/JavaScript browser client; Python 3 standard-library HTTP server; scripted demo in `offline_modes.py`. Optional OpenAI and local Ollama adapters exist but have not been accepted as functioning live features.
- **Requirements:** Python 3; Chrome or Edge; no API key or paid credits for the default demo.

From a GitHub clone or downloaded repository folder (the directory containing `server.py`):

```powershell
git clone https://github.com/kexuanmoonlight-droid/InspirationTrace.git
cd InspirationTrace
py -m unittest discover -p "test_*.py"
py server.py
```

Open **http://127.0.0.1:8765/**. Leave **Scripted Offline Demo** selected. Click **Load Fantasy-Rescue Demo**, then **Send & Continue**; enter **Add dragons to the story**, then **Give the prince and dragons a deeper relationship**. Hover an underlined phrase to highlight its matching evidence card; inspect publisher links, use **Keep as reference** / **Mark reviewed**, restore a version and try **Export Project**. Stop the server with **Ctrl+C**. On Windows, `python` may replace `py`; no third-party Python packages are needed for this demo.

## Development and test evidence

**Key decisions and checks (retrospectively documented; Git commits were uploaded together on 23 Nov 2026):**
- **V4 → V5:** A live API request failed with HTTP 429, so the student chose an explicitly scripted offline fallback; mocked tests were kept separate from live tests ([V5.1 development note](V5_1_CHANGELOG.md)).
- **V5.1:** The third-round relationship request and absent sources led to a prepared V3 branch and two publisher-linked thematic cards; checked with scripted tests ([version evidence upload](https://github.com/kexuanmoonlight-droid/InspirationTrace/commit/2f058c5ea4a302f24b214beceefe5507f3368726)).
- **V5.4:** Student screenshots revealed missing V1 underlines; phrase anchors and regression checks were corrected, then the offline browser flow was accepted ([V5.4 preview upload](https://github.com/kexuanmoonlight-droid/InspirationTrace/commit/f8bb901a25251c07f8b51982ee0e575a24d06720)).
- **V5.5:** The interface and scripted content were translated into English, retaining `legacy_zh/`; 19 automated checks and a mocked-browser check passed, followed by student Windows acceptance ([English UI commit](https://github.com/kexuanmoonlight-droid/InspirationTrace/commit/b2758d7b725e456327d01ac744cdca24550e7d95)).

- [Test report](TEST_REPORT.md): 19 passing automated checks, student-reported English browser acceptance, earlier HTTP 429 API-credit blocker and limits of testing.
- [Development log](DEVELOPMENT_LOG.md): decisions, bugs, corrections and student/AI contributions across versions.
- [Manual testing steps](OFFLINE_TEST_STEPS.md), [version change notes](V5_5_CHANGELOG.md) and [Git commit history](https://github.com/kexuanmoonlight-droid/InspirationTrace/commits/main/).
- [Screenshots](screenshots/), [original V5.4 Chinese JSON test export](evidence/V5_4_Chinese_scripted_test_export.json) and [archived Chinese UI](legacy_zh/) support the reported historical tests; they do not validate live AI.

## Generative AI use declaration — A2

**Student-led, AI-assisted.** The student specified the online-novelist research focus, interaction requirements and author-control goals; identified the third-turn and underline/highlighting defects; decided on the transparent offline fallback after the HTTP 429 credit failure; and carried out Windows browser tests and final acceptance. **OpenAI ChatGPT** substantially assisted with Python/JavaScript implementation, debugging, test preparation, technical documentation, and drafting/revising the A2 report and storyboard. The student reviewed the outputs, requested fixes and checked the prototype; AI was not an autonomous project decision-maker. Automated/mock checks are distinguished from student-run acceptance. The limitations of scripted generation and manually selected sources are disclosed in the linked records.

## Supporting files and submission

The assessed report, storyboard and architecture figures are submitted through the university coursework system; source code, README, tests, changelogs and screenshots are in this public repository. **No separate source-code ZIP or video is required for the repository-based hand-in unless the submission portal explicitly asks for one.** Do not upload API keys, environment files or private exports.
