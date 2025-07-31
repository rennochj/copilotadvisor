# Performance Architecture Analysis Prompt

## Prompt
Analyze the architecture from a performance perspective:

1. **Performance Requirements**
   - Are performance requirements clearly defined (latency, throughput, etc.)?
   - Are SLAs and SLOs specified and achievable?
   - Is there a performance testing strategy?

2. **Scalability Design**
   - How does the system scale horizontally and vertically?
   - Are there any scalability bottlenecks?
   - Is auto-scaling considered and properly designed?

3. **Performance Optimizations**
   - Are caching strategies properly implemented?
   - Is database design optimized for the access patterns?
   - Are there unnecessary network hops or data transformations?

4. **Resource Utilization**
   - Is resource usage (CPU, memory, network) considered?
   - Are there potential resource contention issues?
   - Is the cost-performance trade-off reasonable?

5. **Monitoring & Tuning**
   - Are performance metrics and KPIs defined?
   - Is there adequate performance monitoring?
   - How will performance issues be diagnosed and resolved?

Provide specific recommendations for performance improvements with expected impact.

## Usage
Essential for systems with strict performance requirements or high traffic volumes.