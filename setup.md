# Architecture Advisor - Setup Complete ✓

This project provides architecture guidance and feedback using GitHub Copilot as an AI assistant to review documents, compare them to reference materials, and provide comprehensive feedback.

## Setup Summary

### ✅ GitHub Copilot Instructions
Created `.github/copilot-instructions.md` with:
- Project context and objectives
- Key review principles
- Focus areas for architectural reviews
- Response format guidelines
- Best practices for providing feedback

### ✅ Architectural Review Prompts
Organized in `prompts/` directory by category:
- **General**: Comprehensive and quick assessments
- **Security**: Security architecture and threat modeling
- **Performance**: Performance analysis and scalability
- **Integration**: API design and integration patterns
- **Cloud**: Cloud-native architecture reviews
- **Data**: Data architecture and governance

### ✅ Documentation
- `PROMPTS_GUIDE.md`: Comprehensive guide on using the prompts
- `prompts/README.md`: Quick reference for available prompts

## Next Steps
1. Test the prompts with sample architectural documents
2. Customize prompts based on your organization's standards
3. Add reference architectures for comparison
4. Create templates for common architectural patterns

Modify the instructions to define a process for the review like the following

  - collect design document
  - gather reference information
  - perform preliminary review of the alignment of designs to references
  - prepare questions you may have about the design
  - ask the user to answer questions
  - review the responses to the questions
  - prepare a final review