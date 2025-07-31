# Security Architecture Review Prompt

## Prompt
Conduct a security-focused architectural review addressing:

1. **Security Architecture**
   - Is there a clear security architecture with defined trust boundaries?
   - Are authentication and authorization mechanisms properly designed?
   - How is data protected at rest and in transit?

2. **Threat Modeling**
   - Have potential threats been identified and documented?
   - Are there mitigation strategies for identified threats?
   - Is the attack surface minimized?

3. **Security Controls**
   - Are appropriate security controls in place (WAF, encryption, etc.)?
   - Is there proper input validation and output encoding?
   - Are secrets and credentials managed securely?

4. **Compliance & Privacy**
   - Does the architecture support required compliance standards?
   - Are privacy requirements (GDPR, etc.) considered?
   - Is there appropriate audit logging and monitoring?

5. **Security Operations**
   - Is there a clear incident response plan?
   - How are security updates and patches managed?
   - Are there mechanisms for security monitoring and alerting?

Provide specific security recommendations and highlight any critical vulnerabilities.

## Usage
Use when reviewing architectures that handle sensitive data or have significant security requirements.