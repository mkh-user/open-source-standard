---
title: Open Source Standards
---

# Guide: Open Source Standards

This guide provides step-by-step instructions for creating, organizing, and maintaining a new standard within the OSStd project, following the [Open Source Standards standard](../spec/). It is intended for project maintainers and contributors.

## Prerequisites

As a maintainer-targeted guide this document expects you have:

- A basic understanding of the OSStd project structure and its goals.
- Familiarity with Markdown and YAML front-matter.
- A text editor or IDE configured according to the OSStd project's `.editorconfig`.
- `pre-commit` installed.
- Access to the project repository and permission to create new files and submit pull requests.

## Step-by-Step Instructions

### Determine if a New Standard is Needed

- Identify a clear need for a new standard. Does it address a gap in the project's current guidelines?
- Discuss the idea with other maintainers or open an issue to gather initial feedback. This helps ensure the standard is necessary and has community support.

### Choose a Category and Name

- Decide on the appropriate functional category for your standard. For example:
    - `internals/`: For standards related to the OSStd project's own processes and structure (e.g., this standard).
    - `projects/`: For standards that define how external projects should be structured or maintained (e.g., a standard for `README.md` files).
<!-- markdownlint-disable-next-line MD044 -->
- Choose a short, descriptive name for your standard folder. Use `kebab-case` (e.g., `issue-labels`, `readme`). The name should clearly indicate the standard's purpose. Don't add `-standard` to folder name.

### Create the Standard Folder and Files

- Navigate to the `docs/standards/[category]/` directory in the repository. Create a new category if needed and add `index.md` page with a good icon to it.
- Create a new folder with your chosen name: `docs/standards/[category]/[standard-name]/`.
- Inside this folder, create the necessary files. Every standard **must** include a `spec.md` file. You will also create `guide.md` and, if applicable, `template.md`. Follow the naming convention exactly:
    - `spec.md`: Contains the authoritative rules and requirements.
    - `guide.md`: Provides a practical, step-by-step tutorial.
    - `template.md`: (Optional) Provides a copy-pasteable skeleton.

### Write the Specification

The `spec.md` file is the source of truth. Follow its mandatory structure.

- **Front-matter**: At the very top, include YAML front-matter with `status`, `version`, and `title`.
    - For a new standard, set `status: new` and `version: 0.1`.
    - Example:

        ```yaml
        ---
        status: new
        version: 0.1
        title: Your Standard Title
        ---
        ```

- **Main Title**: Write the main title as `# Spec: [Your Standard Title]`.
- **Core Statement**: In this section, write a concise description of the standard's purpose.
- **Rationale & Constraints**: Explain why the standard exists and any limitations or boundaries it has.
- **Technical Details**: Provide a comprehensive list of requirements, rules, and implementation details. Use subheadings and lists to organize the information clearly.
- **Examples** (Optional): Add concrete examples of the standard in practice.
- **Exceptions** (Optional): Describe any conditions under which the standard may be ignored.

### Write the Guide

The `guide.md` file provides a practical tutorial. Follow its mandatory structure.

- **Front-matter**: Add YAML front-matter with `title`.
    - Example:

        ```yaml
        ---
        title: Your Standard Title
        ---
        ```

- **Main Title**: Write the main title as `# Guide: [Your Standard Title]`. Follow this with a brief overview of what the guide covers and who it is for.
- **Prerequisites**: List any prior knowledge, tools, or resources required to apply this standard. Link to primary sources where helpful.
- **Step-by-Step Instructions**: Break down the process into clear, not-numbered steps. Use `###` for each step header. This prevents broken hash references if steps are later reordered.

    ??? Question "Why "Not-numbered"?"
        It's true instructions are step-by-step and numbered itself, but including numbers in headers means:

        - Magic numbers in hash references (e.g. `..., so you can [jump to next step](./#4-add-badges)`)
        - Breaking hash references or additional diff lines when changing steps

        Because of these issues, it's very important to do not number step headers.

- **Checklist**: End the guide with a summary checklist to verify that the standard has been correctly applied.

### Write the Template (template.md, if applicable)

If your standard provides a fillable template (e.g., a skeleton file for users to copy), include this file.

- **Front-matter**: Add YAML front-matter with `title`.
    - Example:

        ```yaml
        ---
        title: Your Standard Title
        ---
        ```

- **Main Title**: Write the main title as `# Template: [Your Standard Title]`.
- **Template Code**: Include a Markdown code block containing the entire template. Use placeholders like `[PROJECT_NAME]` and `[DESCRIPTION]` where users need to fill in their own information.
- **How to Fill This Template**: Provide a short explanation of what each placeholder means and how to replace it.

### Versioning and Coordination

- The version number is **only maintained in the `spec.md` file's front-matter**.
- When you update a spec (e.g., fix a typo or add a clarification), increment the version appropriately:
    - `patch`: For fixes that do not alter the standard's intent.
    - `minor`: For backwards-compatible additions.
    - `major`: For breaking changes.
- After updating the spec, you **must** review and, if necessary, update the corresponding `guide.md` and `template.md` to stay consistent with the new spec version.

### Submit Your Standard

- Commit your changes to a new branch.
- Open a Pull Request (PR) to the main repository. This is the official process for proposing a new standard or changes to an existing one.
- In the PR description, explain the purpose of the standard and any relevant discussion or background.
- Be prepared to discuss and refine your standard based on feedback from other maintainers.

## Checklist

Use this checklist to verify you have completed all steps for a new standard:

- [ ] A clear need for the standard has been identified and discussed.
- [ ] A category (`internals/` or `projects/`) and a descriptive `kebab-case` name have been chosen.
- [ ] The folder `docs/standards/[category]/[standard-name]/` has been created.
- [ ] `spec.md` has been created with mandatory front-matter (`status: new`, `version: 0.1`, `title`) and all required sections (`Core Statement`, `Rationale & Constraints`, `Technical Details`).
- [ ] `guide.md` has been created with mandatory front-matter (`title`) and all required sections (`Prerequisites`, `Step-by-Step Instructions` with un-numbered headers, `Checklist`).
- [ ] `template.md` has been created (if applicable) with mandatory front-matter (`title`), a Markdown code block for the template, and the `How to Fill This Template` section.
- [ ] The version number is correct in `spec.md` and all files are internally consistent.
- [ ] A Pull Request has been opened to propose the new standard.
