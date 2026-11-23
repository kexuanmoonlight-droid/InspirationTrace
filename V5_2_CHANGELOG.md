# V5.2 — Restore the original underlined evidence-to-source hover interaction

## Requirement that must not regress

The author requested from the outset that **the story's source-related phrase is underlined, and hovering the phrase highlights the corresponding record in the right sidebar**. The right-hand source card should also highlight the corresponding text when hovered/focused. This is a mandatory interaction specification, not an optional decoration.

## Observed defect in V5.1

Although basic hover listeners remained in the source, the practical behavior did not meet the requirement reliably. The existing code marked *entire sections* rather than precise phrases, only focused the first candidate per section, and did not automatically bring the targeted record into view. In the initial fantasy version, cards were deliberately unlinked because the relevant dragon story elements did not yet exist. This made the interaction appear absent during user testing.

## V5.2 changes

- Restored **precise inline underlines**, backed by explicitly configured `highlightText` in source records, rather than underlining the entire outline section.
- Hover/focus on an underlined phrase highlights and scrolls the matching evidence card into view; leave/blur clears temporary highlights. Clicking also focuses the card.
- Hover/focus on a source card also highlights the corresponding outline section and exact underlined phrase.
- Distinct matches and IDs for each of the two fantasy references in the second and third version; the memory trading demo also has one anchored phrase.
- No invented evidence relation on the initial fantasy version, where dragon-related comparison does not match the existing outline. Cards remain visible but unlinked at that stage.
- Kept previous localStorage state key, third-round demo, source URLs, review checkboxes, OpenAI and Ollama modes, and version restore behavior unchanged.
- Added a dedicated regression test for this author-mandated interaction.

## Testing boundary

Automated Python checks verify linked data is in the corresponding story section, event wiring is still present, and existing tests pass. JavaScript syntax check passes. Actual hover rendering, scroll, mouse out, keyboard focus, and visual contrast **require browser retest by the student**.

Candidate URLs are works' pages, not retrieved passages or verified textual overlaps. Underlining denotes *thematic comparison material*, not plagiarism or proof of the model's inspiration.
