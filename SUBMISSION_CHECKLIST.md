# A2 — final submission preparation checklist

Current baseline: InspirationTrace V5.4 accepted as an **offline scripted prototype** by the student on 2026-11-23; an export succeeded. The OpenAI API had insufficient credits and local Ollama remains unverified.

## 1. Prepare public GitHub repository

1. Create a new **public** repository for InspirationTrace (or use an existing one).
2. Before upload, check all text and screenshots for API keys, identifying information, bank or billing details, and any sensitive data. Never upload PowerShell screenshots containing keys.
3. Upload the code and documentation included here. Keep `README.md`, `TEST_REPORT.md`, `DEVELOPMENT_LOG.md`, `OFFLINE_TEST_STEPS.md`, tests and `.gitignore`.
4. Use truthful commits dated when performed: e.g. `Add accepted V5.4 scripted prototype and test records`, then separate subsequent edits. Never fabricate previous commits.
5. From a fresh clone, test `py -m unittest discover -p "test_*.py"`, then `py server.py`, then open `http://127.0.0.1:8765/`. Check sample and export.
6. Save the repository URL, README URL, and links to genuine commits for the A2 report.

## 2. Capture evidence

Collect 2–3 representative, **student-generated** screenshots: first outline, underlined passage + highlighted source card, and reviewed evidence/changed version. Screenshots should show offline scripted mode clearly. Keep exported file evidence if useful, after privacy review.

## 3. Align A2 artefacts (after development freeze)

- Written report: abstract max 300 words, main body max 1100 words, total max 1400, first-page word count per assignment guidance. Confirm exact rules in final brief.
- Storyboard: author idea -> revision -> candidate works/verified links -> evidence hover -> author selection/revision -> version/export. Mark demo-simulated vs future live-model behavior.
- Architecture: browser UI, local Python server, `offline_modes.py` scripted data, storage/export, **optional untested** Ollama and **credit-blocked** OpenAI retrieval/generation boundary.
- AI-assistance and authorship: distinguish student design decisions and actual tests from AI-assisted code/documentation.
- References in APA style aligned with A1; do not imply candidate book pages are model-attributed inspiration sources.

## 4. Final hand-in

Follow the live module hand-in instructions for the project report upload; provide a public working GitHub repository link and README plus any explicitly required attachments. Verify that assessors can open every link without requesting permission. A demo video was not identified as mandatory in the reviewed assignment discussion; check current brief if changed.
