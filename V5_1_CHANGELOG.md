# V5.1 Change log — Closing the scripted prototype loop

## Why (author-observed issue)

During actual V5 manual demonstration the student reported: (1) a first outline and dragon revision were shown, but asking for a closer dragon/prince relationship produced no outline; (2) fantasy scenario lacked visible candidate-source records. These were **script/demo coverage and evidence-dataset limits**, not evidence that a language model was unable to write such a scene.

## Changes implemented by AI assistance, pending student browser acceptance

- Added exactly one **prewritten V3 fantasy revision** for the supported relationship request, with changes across the whole outline rather than an appended note.
- Added **two real, manually located and verified bibliographic/product pages** to fantasy demo's right evidence sidebar; do not imply real-time retrieval or underlying text matching.
- Source card descriptions compare only elements supported by public descriptions. *The Priory of the Orange Tree* is a relatively closer dragon/politics theme; *The Hobbit* is a much broader dragon/adventure comparison. Neither is identified as a model's actual source.
- V1, which lacks dragons, shows cards as browsing candidates with **no section linkage** until a dragon-related V2/V3 is displayed.
- Preserve manually selected and reviewed flags if the user refreshes curated evidence on the **same version**.
- Changed browser storage namespace to avoid a V5.0 prior session confusing V5.1 acceptance.
- Kept API / Ollama pathways, existing versioning, and no-source policy for unsupported scenarios.

## Verification boundary

- `python -m unittest discover -v`: **14/14 automated checks passed in development environment**, including two added V5.1 tests.
- JavaScript syntax checked with `node --check`.
- Real browser manual acceptance F01–F10 and clicks to live publisher pages: **awaiting student execution**.
- OpenAI generation: **Blocked / HTTP 429 credit balance exhausted** in the student's previous attempt.
- No automated open-ended creative capability, reliable real-time similarity ranking, or plagiarism assessment is claimed for Offline Demo.

## Development/authorship

The research and intended features were defined by the student; failure observations and the requirement to expose real links were student-reported requests. AI assistance implemented the scripted third revision, data wiring, tests, and documentation; the student needs to run browser checks and independently record what worked. Do not present AI-authored changes as independently implemented by the student.
