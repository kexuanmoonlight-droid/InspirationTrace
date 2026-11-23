# InspirationTrace V5.5 EN — Offline Demo / Local Ollama / OpenAI

**Status:** research prototype. V4 is preserved separately; this is a new branch/version. No API credit is required for the default offline demo.

## Quick start on Windows

1. Extract the complete ZIP (do not run inside the ZIP). Open the folder with `server.py`.
2. In File Explorer press **Alt + D**, type `powershell`, press Enter.
3. Run `py test_offline_modes.py` (optional), then `py server.py`.
4. Open **http://127.0.0.1:8765/** in Chrome or Edge.
5. In the **Run Mode** selector, leave **Scripted Offline Demo** selected. Choose a scenario button, press **Send & Continue**, then review the outline and sidebar.
6. Test the scripted second round with the fantasy example: after generating V1, type **Add dragons to the story**. The prepared V2 changes the main plot and keeps V1 recoverable. This is a **pre-authored demonstration**, not arbitrary AI generation.

**If V4 is already running on port 8765:** press `Ctrl+C` in the old PowerShell terminal first. Start V5 afterward. The two projects should not run on the same port simultaneously.

**Cost and privacy:** default offline demo uses no paid calls and never sends story text to a remote model. A demo URL to a public publisher page opens in your browser only when clicked. User messages/outlines are stored in your browser's local storage. Export JSON if you want backups. Switching modes does not remove old drafts.

## Three modes

| Mode | Description | Limitations |
|---|---|---|
| **Offline scripted demo** (default) | Three prepared story outlines, two prepared example revisions, optional manually curated publisher comparison, version restore, review and reference selection | **Not a generative AI.** Unknown messages do not produce made-up results; not an originality detector. |
| **Ollama local AI** | A downloaded local model generates free-form multi-turn story text and updates outlines, using the same editor | Requires downloading/installing Ollama and model weights, enough RAM/disk; performance unverified on the user's computer; no live evidence retrieval in this mode. |
| **OpenAI API** | Original V4 cloud generation and search path remains available | Requires usable API credit and is billed separately; not tested end-to-end here. |

### Optional: local Ollama

Ollama is **not included** in this ZIP. After installing it from the official provider (https://ollama.com/), use a terminal to fetch a model, for example:

```powershell
ollama pull qwen2.5:3b
ollama list
```

Default local model: `qwen2.5:3b`. To change it, set `$env:OLLAMA_MODEL="your-model-name"` before `py server.py`. Local endpoint defaults to `http://127.0.0.1:11434`; configurable with `OLLAMA_URL`. Choose **Local Ollama Model** in the site. The app checks `/api/tags` and reports if the model isn't installed. The local model may generate malformed JSON or poor prose, depending on its size and capabilities. There is **no fallback to cloud billing** when it fails.

Optional cloud mode is enabled by configuring `OPENAI_API_KEY` in your terminal (do not paste a key into source files or GitHub). Switch the browser selector to the cloud mode. To reduce cost, turn off the checkbox for auto-search while testing story generation.

## Core UI behavior

- Left upper panel shows the current story outline and versions.
- Left lower panel is the conversation area.
- Right sidebar shows candidate works, available source links, selected references, and reviewed status.
- Clicking underlined outline text focuses the corresponding evidence card when an association exists.
- The fantasy demo now includes two manually curated thematic candidate cards, with broad V1 phrase links and more specific V2/V3 phrase links; the memory-city demo features one **manually prepared thematic comparison** to *The Memory Police* with a real publisher product page. It **does not prove** the model used that book or that there is substantive text overlap. The future-letter demo has no candidate sources.
- In offline fantasy and memory demos, annotation is **phrase-level thematic linkage**, not textual-match detection; other modes may have no exact phrase anchors.
- Each update creates a recoverable version; the browser holds chat history locally. Beware: restoring a version does not yet branch the chat history, which could introduce irrelevant earlier discussion in future local/cloud calls.

## Important evidence and research limits

- `selected` means the author opted to keep a link as reference. `reviewed` means the user marked it seen; neither indicates the work is verified as an inspiration or is original.
- A source URL pointing to a publisher page does not verify a similarity statement, nor that the model consulted that work.
- The scripted demo does **not** perform external similarity search, inspect whole works, track training data, determine plagiarism, or evaluate whether authors make more accurate originality decisions.
- The optional Ollama mode generates live fiction but has **no automatic similarity retrieval**. Any existing evidence records associated with another version must not be reused as though they had been reverified.

## Files

- `server.py`: standard-library local HTTP service and V4 cloud endpoints, plus new mode routing.
- `offline_modes.py`: explicit scripted mode and optional local Ollama adapter.
- `index.html`: user interface with mode selector, conversation, outline, evidence sidebar.
- `test_backend_v4.py`: preserved V4 mock contract tests.
- `test_offline_modes.py`: new tests for demo behavior and no fake source assertions.
- `TEST_REPORT.md`: executed checks, the observed HTTP 429 billing blocker, pending test statuses and validation boundaries.
- `DEVELOPMENT_LOG.md`: chronological record of student design decisions, AI-assisted implementation changes, A1/A2 report corrections and what has or has not been personally tested.
- `OFFLINE_TEST_STEPS.md`: hands-on V5 scripted demonstration acceptance cases.

## Coursework / AI assistance disclosure

This V5 adaptation was AI-assisted. The user defined the fixed scope (multi-turn creative dialog plus evidence sidebar), discovered V4's API-credit blocker, and approved an offline fallback and optional local model route. The generated modifications and automated tests still require the student to run real browser checks before claiming personal verification. This document is not a substitute for the student's own test log.


## V5.1 close-loop update

See `V5_1_CHANGELOG.md` and `OFFLINE_TEST_STEPS.md`. The fantasy offline script now supports three **fixed** outline rounds (initial → dragons → prince/dragon relationship). Its right sidebar shows two real, manually verified book-page URLs; these are thematic references, **not** search results, computed similarity, proof of copying, or LLM provenance. Public links still require the reviewer to inspect the page. V5.4 browser acceptance was subsequently reported by the student. This does not expand offline mode to unrestricted multi-turn AI conversation.

## Important V5.2 preserved interaction: underline ↔ sidebar hover

When an outline passage has manually curated relevant comparison material, the **specific linked phrase is underlined**. Hovering or keyboard-focusing that phrase highlights its corresponding record in the right sidebar; hovering/focusing the record highlights the corresponding outline text. These links denote **thematic comparison prompts**, not verified textual similarity or model provenance. This was an original design requirement restored in V5.2 after a V5.1 user-observed regression. See `V5_2_CHANGELOG.md` and `test_hover_link_regression.py`.

## V5.4 fix after student screenshot

The student found that V1 displayed source cards with no underlines. Root cause: the earlier demo code intentionally assigned **no V1 anchors**, so hover highlighting could not activate. This version adds two **explicitly broad** V1 theme anchors, keeps the existing V2/V3 anchors, and re-fetches incomplete old saved annotation metadata without erasing review checkboxes. The visible heading includes **V5.4** to help verify that the new server is running. See `V5_4_CHANGELOG.md`. Run `py -m unittest discover -p "test_*.py"` to execute regression tests. Browser recheck on the student's own computer remains required.


## Final V5.4 student acceptance and hand-in preparation

On 23 November 2026, the student reported a successful end-to-end walkthrough and file export on V5.4 with no observed issues. This is acceptance of the **offline scripted demonstration**, not verification of unrestricted LLM dialogue or automatic similarity retrieval. See [TEST_REPORT.md](TEST_REPORT.md) for the evidence boundary and [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) for the GitHub and A2 hand-in workflow.


## V5.5 EN — English-language interface and demonstration content (23 Nov 2026)

**Current default version: V5.5 EN.** The original, student-accepted Chinese V5.4 UI and scripted data remain in `legacy_zh/` and were **not overwritten**. The new interface, outline text, scripted assistant messages, comparison descriptions, feedback, mode labels and demo prompts are in English. The original user-designed mechanics remain unchanged: outline/side-panel underlines, bidirectional hover and keyboard-focus highlights, independent versions and review/reference flags, export to JSON, and three mode choices.

**Three-round English fantasy demo** (free, pre-written, *not* generative AI):
1. Click **Load Fantasy-Rescue Demo** and **Send & Continue**.
2. Type **Add dragons to the story**; send and confirm V2.
3. Type **Give the prince and dragons a deeper relationship**; send and confirm V3.
4. Hover an **underlined phrase**; verify the corresponding publisher-linked card highlights. Hover the card to highlight the phrase. Check **Keep as reference** and **Mark reviewed**, restore a version, and export JSON.

The two comparison candidates retain their genuine publisher URLs. They are **manually curated thematic analogies**, *not* computed similarities, plagiarism detections or model-used citations. The English revision cannot turn scripted demonstration responses into live LLM behaviour.

**Migration:** This English build uses new browser local-storage keys (`inspirationtrace-chat-evidence-v5-5-en` and `inspirationtrace-v5-5-en-mode`) to avoid showing saved Chinese stories inside English examples. Old V5.4 browser data are not erased; exported JSON remains the durable record. Exported V5.4 JSON is a historical Chinese test artefact and should not be represented as English-generated output.

**Testing:** 19 Python checks passed after adapting expected language; an automated Chromium DOM interaction walkthrough using mocked Python API responses confirmed V1–V3 phrase anchors, sidebar highlights, and review checkboxes. The user's **own** Windows browser acceptance of V5.5 English remains pending. Previous V5.4 student acceptance remains valid for V5.4 only.

**Project evidence:** `screenshots/v5_4_chinese_accepted_hover.png` and `screenshots/v5_4_chinese_accepted_conversation.png` are user-supplied screenshots of the preceding accepted Chinese prototype. `screenshots/v5_5_english_browser_smoke.png` is an automated browser test render, *not* a screenshot of a student-run acceptance test.
