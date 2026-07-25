---
status: new
version: 0.1
title: Open Source Standards
---

# Spec: Open Source Standards

Specification for the structure, lifecycle, and content of all standards within the OSStd project.

## Core Statement

This standard defines the mandatory framework for creating, organizing, and maintaining all standards documents within the **Open Source Standard** project. It establishes a consistent format and a clear lifecycle to ensure that every standard is understandable, reviewable, and reliable for users and contributors.

## Rationale & Constraints

A project that defines standards must itself operate under a clear and predictable methodology. Without a meta-standard, the project risks inconsistency, making its own standards difficult to follow and trust.

- **Rationale**: This standard ensures uniformity across all documents, simplifies the contribution process, and clearly communicates the maturity level of each standard to its users.
- **Constraints**: All new standards **must** adhere to this framework before being accepted. The structure is designed to be scalable but is mandatory for the project's internal consistency.

## Technical Details

This standard specifies a three-part structure for every standard, stored in dedicated subdirectories under the `docs/standards/` folder.

### Directory Structure

- All project documentation is stored in the `docs/standards` directory.
- Each standard is composed of up to three files, all in a folder stored in its respective category folder:
    - `docs/standards/[category]/[standard-name]/spec.md`
    - `docs/standards/[category]/[standard-name]/guide.md`
    - `docs/standards/[category]/[standard-name]/template.md` (if applicable)

### File Naming and Categorization

- Standards are organized by functional category (e.g., `internals/` for OSStd-related, `projects/` for project-scope standards).
- Folder names should be short, descriptive, and in `kebab-case` (e.g., `open-source-standards`).

### Content Structure of Each Component

#### Guide (`guide.md`)

- **Purpose**: A practical, step-by-step tutorial that explains how to apply the standard from scratch. It is written for implementers and end-users (depend on what standard is for).
- **Mandatory Sections**:
    - front-matter (YAML) with `title`.
    - `# Guide: [Standard Title]` – Main title. Followed by a brief overview of what the guide covers and who it is for.
    - `## Prerequisites` – Any prior knowledge or tools required, linked to primary sources got get ready.
    - `## Step-by-Step Instructions` – **Not-numbered** steps (e.g., `### Create the directory...`, `### Write the spec file...` (*without `...`*)).

        ??? Question "Why "Not-numbered"?"
            It's true instructions are step-by-step and numbered itself, but including numbers in headers means:

            - Magic numbers in hash references (e.g. `..., so you can [jump to next step](./#4-add-badges)`)
            - Breaking hash references or additional diff lines when changing steps

            Because of these issues, it's very important to do not number step headers.

    - `## Checklist` – A summary checklist to verify completion.
- **Tone**: Instructional, clear, and direct.

#### Spec (`spec.md`)

- **Purpose**: The authoritative reference document containing all rules, requirements, and rationale. This is the "source of truth."
- **Mandatory Sections** (as defined in this standard):
    - front-matter (YAML) with `status` (for new or deprecated standards), `version`, and `title`.
    - `# Spec: [Standard Title]` – Main title.
    - `## Core Statement` – Concise description of the standard's purpose.
    - `## Rationale & Constraints` – Explanation of why the standard exists and its limitations.
    - `## Technical Details` – Comprehensive list of requirements, rules, and implementation details.
    - `## Examples` (Optional) – Concrete examples of the standard in practice.
    - `## Exceptions` (Optional) – Conditions under which the standard may be ignored.
- **Tone**: Formal, precise, and definitive.

#### Template (`template.md`)

- **Purpose**: Provides a copy-pasteable skeleton (as a Markdown code block) that implements the standard. It is only created when applicable.
- **Mandatory Sections**:
    - front-matter (YAML) with `title`.
    - `# Template: [Standard Title]` – Main title.
    - A Markdown code block containing the entire template (e.g., a skeleton `README.md`, a `.github/ISSUE_TEMPLATE.md`, etc.).
        - When a template contains multiple code files, level 2 headings *must* be added before each one to show what is it and a **horizontal rule** after each one.
    - `## How to Fill This Template` – A short explanation of what each placeholder (e.g., `[PROJECT_NAME]`) means and how to replace it.
- **Tone**: Concise and instructional.

### Versioning and Coordination Across Components

- The **version number is only maintained in the `Spec` file** (in its front-matter).
- The `Guide` and `Template` (if present) **must be updated to match the latest version** of the Spec. They do not contain version numbers themselves.
- When a Spec is updated, the corresponding Guide and Template must be reviewed and updated accordingly to stay consistent.

### Standard Lifecycle and Versioning

- **New**: A standard under initial development or open for feedback (`status: new`).
    - **Version**: `0.1`. Increment `minor` for significant rewrites. `patch` increments are not used for new standards.
    - **Usage**: Not recommended for production use.
- **Active**: The standard is finalized and approved (no `status` front-matter).
    - **Version**: `1.0`. Follows Semantic Versioning (`major.minor.patch`).
    - **Changes**: `major` for breaking changes, `minor` for backwards-compatible additions, `patch` for fixes that do not alter the standard's intent (e.g., typo fixes, rephrasing for clarity).
- **Deprecated**: The standard is no longer recommended (`status: deprecated`).
    - **Maintenance**: No further updates. If reactivated, it must be under a new `major` version to maintain clarity.

## Examples

- **Standard with a Template**:
    - **Standard**: "README Standard" (`specs/projects/readme.md`)
    - **Guide**: Provides steps to write a README, including how to structure sections, choose a badge, and write an introduction.
    - **Template**: Provides a skeleton `README.md` file with placeholders like `[PROJECT_NAME]`, `[DESCRIPTION]`, `[USAGE]`, etc.
- **Standard without a Template**:
    - **Standard**: "Issue Labels Standard" (`specs/projects/issue-labels.md`)
    - **Guide**: Explains how to create and apply labels in GitHub's web interface.
    - **Template**: Not applicable, as the implementation is not a text file but a GUI action.

## Exceptions

- A standard may be granted an exception to this structure (e.g., skipping the `Guide` or `Template`) by a project maintainer if a strong, documented justification is provided.
- A new standard may be granted to don't include `status: new` by a project maintainer if:
    - It doesn't need to be actively open for feedback for any time range.
    - **Or** a strong and documented justification is provided.
