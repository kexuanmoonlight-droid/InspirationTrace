# V5.4 — V1 hover/underline missing: narrow fix

**Student-observed failure:** V1 of fantasy rescue displayed two source cards but no underlines, even after hard refresh.

**Actual cause:** the scripted `demo_evidence()` deliberately returned no `highlightText` or `sectionIndex` for V1. Earlier tests allowed that, so this was not a browser-cache problem.

**Change:** two V1 **broad thematic** exact-phrase anchors now map to the existing publisher-linked source cards; old saved source metadata with missing anchors is refreshed; browser title and header now show V5.4. Existing V2/V3, card links, review flags, versions, API/Ollama paths remain unchanged.

**Validation:** 19 Python unit tests and JS syntax pass. Chromium UI DOM hover smoke test passes with actual HTML and precomputed V1 data. Student full UI acceptance pending.

**Meaning of evidence:** V1 does not mention dragons. The new links only compare broad political-intrigue and rescue/adventure motifs; they do **not** establish text similarity, copying, or model-used provenance.
