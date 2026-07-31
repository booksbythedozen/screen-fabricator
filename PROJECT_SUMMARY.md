# Screen Fabricator Project Summary

## Project Overview

Screen Fabricator is a Streamlit-based application that enables clinicians, researchers, and other subject-matter experts to create custom screening, intake, triage, and decision-support tools without programming.

The project was initiated by Bryce P Mulligan, PhD, CPsych.

## Origin Story

The project began as an exploration of whether configurable mental health screening tools could be created by non-programmers.

An important guiding assumption was that many future users would have little or no software-development experience.

The core goal became:

> Enable subject-matter experts to encode clinical knowledge without becoming programmers.

Throughout development, the project evolved from a simple questionnaire builder into a flexible screening and triage platform capable of supporting a wide variety of workflows.

---

## V03: Questionnaire Builder Era

V03 focused primarily on:

- Building questionnaires
- Defining questions
- Creating referral pathways
- Simple screening workflows

Primary audience:

- Community organizations
- Community health programs
- Educational users

Key characteristics:

- Plain-language scoring descriptions
- Community-focused orientation
- Educational emphasis
- Early tool-management functionality

This version demonstrated that non-programmers could create structured screening workflows using a guided interface.

---

## V04: Functional Screening Platform

V04 represented a major architectural milestone.

Key additions included:

- Symptom Elevation framework
- Safety Alert framework
- Questionnaire-Based Scoring
- Total Score Entry workflows
- Safety Indicator items
- Configurable scoring thresholds
- Scoring Simulator
- Tool-level instructions

This release established the core architecture that continues to underpin Screen Fabricator.

### Major Architectural Innovation

V04 explicitly separated:

**Symptom Elevation**

from

**Safety Risk**

This made it possible for a user to have:

- Low Symptom Elevation
- Moderate Symptom Elevation
- High Symptom Elevation

while also independently triggering:

- Immediate Safety Concern

This remains a foundational design principle of the application.

---

## Key Feedback Following V04

Following hands-on testing of V04, several themes emerged.

### Home Page Orientation

Users wanted:

- Better onboarding
- Clear authorship information
- Intended-use statements
- Limitations and disclaimers
- Workflow guidance
- Tutorial or example content

This ultimately led to the much richer Home page included in V07.

### Meaningful Safety Logic

The original Total Score Entry workflow relied on manually triggering a safety concern.

Feedback suggested that users should instead be able to define:

- Critical items
- Critical-item thresholds

Example:

- PHQ-9 Total Score
- PHQ-9 Item 9 score

A Safety Alert should be triggered automatically if a critical-item threshold is exceeded.

This directly led to the Critical Item framework implemented in later versions.

### More Prominent Safety Alerts

Safety information needed to be visually impossible to miss.

This eventually resulted in the larger Safety Alert presentation used in V07.

### Numeric Input Preferred

For clinical workflows, testers preferred:

- Numeric-entry fields

over:

- Sliders

This reflected a preference for precision and efficiency.

### Collaboration and Sharing

Early questions emerged regarding:

- Saving tools
- Sharing tools
- Version control
- Collaboration
- Import and export functionality

These discussions ultimately contributed to the JSON export functionality introduced later.

---

## Developer Context

An important factor in the project's design is that its creator does not have formal software-development training.

Background:

- Strong understanding of clinical workflows
- Strong understanding of screening concepts
- Working knowledge of R
- First Streamlit application

This reality shaped a core project philosophy:

> If a clinician cannot understand a feature intuitively, the feature should be simplified.

As a result, the application consistently prioritizes:

- Plain language
- Visible guidance
- Workflow-oriented design
- Minimal technical jargon

over software-developer conventions.

---

## Design Principles

Several principles have emerged repeatedly throughout development.

### No Programming Required

Users should never need to write code in order to build a screening tool.

### Transparency Over Complexity

The application should make it easy to understand:

- Questions
- Scoring
- Thresholds
- Safety rules
- Recommendations

### Clinician-First Design

Features should be understandable to:

- Psychologists
- Physicians
- Nurses
- Allied health professionals
- Researchers
- Community volunteers

### Safety-Conscious Design

Safety Alerts should remain separate from symptom-severity classifications.

### Visible Guidance

Whenever possible:

- Visible guidance is preferred

over

- Hidden tooltips
- Technical documentation
- Assumed knowledge

---

## Documentation Philosophy

As development progressed, it became clear that documentation was becoming as important as code.

The project evolved from:

- Generating scripts

to

- Generating scripts plus documentation

For major releases, the desired deliverables became:

- Application code
- Development plan
- Pilot-testing materials
- Change log
- Roadmap

Documentation is considered a first-class project artifact.

---

## Pilot Testing

A formal pilot-testing process was established.

Pilot testers were encouraged to:

1. Build a screening tool.
2. Configure symptom-elevation thresholds.
3. Configure safety items.
4. Use the tool.
5. Review outputs and recommendations.
6. Export a tool definition.

Feedback is categorized as:

### Bugs

Something does not work correctly.

### Usability

Something works but is confusing or unnecessarily complicated.

### Enhancements

A new capability or improvement that may be valuable in future versions.

---

## Tool 
