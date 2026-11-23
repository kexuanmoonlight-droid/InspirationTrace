# V5.5 EN — English-language hand-in interface

**Request:** After accepting the V5.4 interaction, the student requested an English-language interface and asked for the associated code changes to be reflected in the public GitHub repository.

**Preserved:** original V5.4 Chinese source is backed up under `legacy_zh/`. The intended open-ended AI collaboration remains the design goal; the offline demo is explicitly scripted. Bidirectional underline ↔ source-card hover/focus, version restore, reference selection, review flags, publisher URLs, JSON export, and OpenAI/Ollama adapters remain.

**Changes:** all visible labels, prompts, notices, scripted three-round fantasy outline and two further example scripts, scripted responses and source descriptions are now English. Backend validation and service notices are also English. English phrase anchors were individually re-mapped for V1/V2/V3.

**Regression evidence:** 19/19 Python tests passed in this environment. JS syntax check passed. Chromium UI smoke test used intercepted/mock API responses and confirmed two exact anchors and two cards at each of V1, V2 and V3, hover highlights in both directions, and a review checkbox. The actual Windows browser run of English V5.5 is **pending**; it must not be reported as personally verified.

**Screenshots:** student-supplied Chinese V5.4 accepted screenshots are retained as historical test evidence, clearly labelled; English smoke render is distinct from user acceptance.

**Limitations:** API HTTP 429 insufficient credits remains unresolved for real cloud generation; live source retrieval and open-ended LLM dialogue are not verified. Two curated publisher pages do not establish originality or text-level similarity.
