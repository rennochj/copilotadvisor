# Architecture Review Prompts Guide

This guide explains how to effectively use the architectural review prompts with GitHub Copilot.

## Overview
The prompts are organized by focus area to help you conduct targeted architectural reviews. Each prompt is designed to elicit specific, actionable feedback from GitHub Copilot.

## Directory Structure
```
prompts/
├── general/          # General architecture reviews
├── security/         # Security-focused reviews
├── performance/      # Performance analysis
├── integration/      # Integration architecture
├── cloud/           # Cloud-specific reviews
└── data/            # Data architecture
```

## How to Use the Prompts

### 1. Select the Right Prompt
Choose a prompt based on your review needs:
- **Structured Review Process**: For systematic, interactive reviews with Q&A
- **Comprehensive Review**: For full architectural assessments
- **Quick Assessment**: For rapid reviews or initial feedback
- **Specialized Reviews**: For focused analysis (security, performance, etc.)

### 2. Prepare Your Content
Gather the architectural artifacts you want to review:
- Architecture diagrams (as images or descriptions)
- Design documents
- Technical specifications
- Code structure overviews

### 3. Using with GitHub Copilot

#### In VS Code:
1. Open GitHub Copilot Chat (Ctrl+Shift+I or Cmd+Shift+I)
2. Copy the relevant prompt from the prompts directory
3. Paste the prompt into the chat
4. Attach or paste your architectural content
5. Submit and wait for the analysis

#### Best Practices:
- Provide context about your project's constraints
- Include relevant diagrams or documentation
- Be specific about areas of concern
- Ask follow-up questions for clarification

### 4. Combining Prompts
For comprehensive reviews, combine multiple prompts:
1. Start with a general assessment
2. Deep dive into specific areas (security, performance)
3. Focus on integration points if applicable
4. Review data architecture separately

## Example Workflow

```markdown
1. Initial Review (Choose One):
   - Use general/structured-review-process.md for interactive review
   - Use general/comprehensive-review.md for single-pass assessment
   - Use general/quick-assessment.md for rapid feedback

2. Deep Dives:
   - If security concerns → use security/security-review.md
   - If performance critical → use performance/performance-analysis.md
   - If many integrations → use integration/integration-review.md

3. Specialized Reviews:
   - Cloud deployment → use cloud/cloud-architecture.md
   - Data-intensive → use data/data-architecture.md

4. Follow-up:
   - Ask specific questions based on feedback
   - Request examples or alternatives
   - Clarify recommendations
```

### Structured Review Process Example
When using the structured review process:
1. **Submit Design**: Provide your architecture document
2. **Initial Analysis**: Copilot analyzes and compares to references
3. **Answer Questions**: Respond to clarifying questions
4. **Final Review**: Receive comprehensive feedback based on full context

## Tips for Better Results

### Provide Clear Context
- Explain the business domain
- Describe constraints and requirements
- Mention technology preferences or restrictions

### Be Specific
- Highlight areas of particular concern
- Mention specific standards or frameworks to follow
- Indicate if this is greenfield or brownfield

### Iterate on Feedback
- Don't accept the first response as final
- Ask for clarification or alternatives
- Request specific examples
- Challenge recommendations if needed

### Document Decisions
- Save important feedback
- Create decision records based on recommendations
- Track which suggestions were implemented

## Creating Custom Prompts

Feel free to create custom prompts for your specific needs:

1. Copy an existing prompt as a template
2. Modify for your specific requirements
3. Save in the appropriate category
4. Test with sample architectures

### Custom Prompt Template
```markdown
# [Your Review Focus] Prompt

## Prompt
[Your specific review instructions focusing on:]

1. **[Aspect 1]**
   - [Specific questions]
   - [What to analyze]

2. **[Aspect 2]**
   - [Specific questions]
   - [What to analyze]

[Additional instructions]

## Usage
[When and how to use this prompt]
```

## Prompt Maintenance

- Review and update prompts based on experience
- Add new prompts for emerging patterns
- Remove or consolidate redundant prompts
- Share effective prompts with the team

## Integration with Development Workflow

1. **Design Phase**: Use comprehensive review prompts
2. **Implementation**: Use quick assessments for decisions
3. **Code Review**: Reference architectural feedback
4. **Retrospectives**: Update prompts based on lessons learned

Remember: These prompts are tools to augment your architectural review process. Always apply critical thinking and consider your specific context when evaluating Copilot's feedback.