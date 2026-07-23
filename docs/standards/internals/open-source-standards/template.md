---
title: Open Source Standards
---

# Template: Open Source Standards

## Specification

```markdown
---
status: new
version: 0.1
title: [STANDARD_TITLE]
---

# Spec: [STANDARD_TITLE]

[One or two sentences explaining what this standard specifies.]

## Core Statement

[A concise paragraph describing the standard's purpose. Explain what problem it solves and why it matters.]

## Rationale & Constraints

[Generally explain why this standard exists and what its boundaries are.]

- **Rationale**: [Why is this standard necessary? What benefits does it provide?]
- **Constraints**: [What are the limitations or scope of this standard? What does it not cover?]

## Technical Details

[Provide the comprehensive rules, requirements, and implementation details. Use subheadings and lists as needed.]

### [Subheading 1]

- [Requirement or rule]
- [Another requirement]

### [Subheading 2]

- [Requirement or rule]
- [Another requirement]

## Examples (Optional)

[Add concrete examples of the standard in practice. This could be a small code snippet, a diagram, or a reference to an external example.]

[Remove the "(Optional)" notice or remove entire section.]

## Exceptions (Optional)

[Describe any conditions under which this standard may be ignored or modified.]

[Remove the "(Optional)" notice or remove entire section.]
```

---

## Guide

```markdown
---
title: [STANDARD_TITLE]
---

# Guide: [STANDARD_TITLE]

[One or two sentences explaining what this guide covers and who it is for. Reference the spec where appropriate.]

## Prerequisites

- [List any prior knowledge, tools, or resources needed.]
- [For example: Familiarity with Markdown, access to the repository, etc.]

## Step-by-Step Instructions

### [Step 1 Header – Without Numbering]

[Explain what to do in this step. Include commands, examples, or screenshots if helpful.]

### [Step 2 Header – Without Numbering]

[Continue with clear, actionable instructions.]

### [Step 3 Header – Without Numbering]

[Continue until all steps are covered.]

## Checklist

Use this checklist to verify that the standard has been correctly applied:

- [ ] [Item 1 to check]
- [ ] [Item 2 to check]
- [ ] [Item 3 to check]
```

---

## Template

````markdown
---
title: [STANDARD_TITLE]
---

# Template: [STANDARD_TITLE]

[If this template contains multiple files, add level 2 headings before each one and separate them with horizontal rules.]

```markdown
[TEMPLATE_CONTENT_HERE]
```

---

## How to Fill This Template

1. **[Step title in bold]**: [Describe step here.]

2. **[Step title in bold]**: [Describe step here.]

    - [Use list if needed]
````

## How to Fill This Template

1. **Replace Placeholders**: Throughout the template, replace all `[...]` placeholders with the actual values for your standard. Use `kebab-case` for folder and file names, but `Title Case` for the title itself.

2. **Follow the Spec**: Ensure that the `spec.md` file you create from this template follows all the rules defined in [the "Open Source Standards" spec](../spec/). Pay special attention to:
   - The YAML front-matter (`status`, `version`, `title`).
   - Including all required sections (`Core Statement`, `Rationale & Constraints`, `Technical Details`).

3. **Guide Consistency**: The `guide.md` is a practical tutorial. Make sure the steps are clear and actionable. The guide **must not** contain a version number; it will always reflect the latest version of the corresponding spec.

4. **Review and Refine**: Before submitting a pull request, review your standard files to ensure they are internally consistent and adhere to the project's tone and style.

5. **Submit a PR**: Propose your new standard by opening a Pull Request to the main repository.
