# Integration Architecture Review Prompt

## Prompt
Review the integration aspects of the architecture:

1. **Integration Patterns**
   - Are appropriate integration patterns used (sync/async, messaging, etc.)?
   - Is the coupling between systems appropriate?
   - Are integration points clearly defined?

2. **API Design**
   - Are APIs well-designed and following standards (REST, GraphQL, etc.)?
   - Is there proper API versioning strategy?
   - Are API contracts clearly defined?

3. **Data Integration**
   - How is data consistency maintained across systems?
   - Are there clear data ownership boundaries?
   - Is data synchronization strategy appropriate?

4. **Error Handling**
   - How are integration failures handled?
   - Are there retry mechanisms and circuit breakers?
   - Is there proper error logging and monitoring?

5. **External Dependencies**
   - Are external system dependencies clearly documented?
   - What happens when external systems are unavailable?
   - Are SLAs with external providers considered?

Highlight integration risks and provide recommendations for robust integration architecture.

## Usage
Critical for systems with multiple integrations or in microservices architectures.