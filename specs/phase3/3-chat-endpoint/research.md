# Research: Chat Endpoint with OpenAI Agent

**Feature**: Phase III Module 3 - Chat Endpoint
**Date**: 2026-01-23
**Spec**: [spec.md](./spec.md)

## Research Summary

This document consolidates research findings for implementing the chat endpoint with OpenAI Agent integration. All "NEEDS CLARIFICATION" items from the plan template have been resolved.

## OpenAI Agent SDK Research

### Decision: Use OpenAI Assistants API
**Rationale**: The OpenAI Assistants API is the most mature and well-documented approach for creating AI agents that can use tools. It provides built-in support for tool calling and conversation history management.

**Alternatives considered**:
- OpenAI Chat Completions API with function calling: More manual work required for conversation state management
- LangChain agents: Adds complexity with additional dependencies
- Custom agent implementation: Would require significant development effort

### Integration Pattern
The integration will follow this pattern:
1. Load conversation history from database
2. Format messages for OpenAI API (user, assistant, system roles)
3. Configure assistant with MCP tools
4. Run assistant thread with user message
5. Store both user and AI messages in database

## MCP Server Integration Research

### Decision: Subprocess stdio Transport
**Rationale**: The existing MCP server (`mcp_server.py`) is already implemented and working with stdio transport. We can connect to it programmatically using the MCP SDK's client capabilities.

**Integration approach**:
- Use `mcp.client` to connect to the MCP server
- Register MCP tools as OpenAI-compatible tools
- Pass user_id context to ensure proper authorization

### Tool Mapping
The 5 MCP tools from Module 2 map directly to OpenAI tools:
- `add_task` → OpenAI tool for creating tasks
- `list_tasks` → OpenAI tool for listing tasks
- `complete_task` → OpenAI tool for marking tasks complete
- `delete_task` → OpenAI tool for deleting tasks
- `update_task` → OpenAI tool for updating tasks

## Database Transaction Research

### Decision: Load Conversation History Per Request
**Rationale**: Aligns with the stateless design requirement from the constitution (XV. Stateless Chat Design). Loading history from DB ensures consistency across server instances and survives server restarts.

**Implementation approach**:
- Query `messages` table ordered by `created_at` for each conversation
- Limit to reasonable number of messages (e.g., last 50) to prevent performance issues
- Format messages as OpenAI-compatible message array

### Performance Considerations
- Add database indexes for efficient message retrieval
- Implement pagination for very long conversations
- Cache recent conversation history if needed

## Authentication Research

### Decision: Reuse Existing JWT Middleware
**Rationale**: The existing JWT authentication system from Phase II Module 3 is robust and well-tested. Reusing it maintains consistency and reduces implementation complexity.

**Implementation approach**:
- Apply existing `get_current_user` dependency to chat endpoints
- Verify JWT token user_id matches URL user_id parameter
- Pass user_id to MCP tools for authorization

## OpenAI API Best Practices

### Error Handling
- Implement retry logic for transient API failures
- Gracefully handle rate limits with exponential backoff
- Return user-friendly error messages instead of raw API errors

### Rate Limiting
- Monitor API usage and implement client-side rate limiting
- Consider implementing server-side rate limiting per user
- Queue messages during high traffic periods

### Message Context Limits
- Implement intelligent context window management
- Summarize older conversation history when approaching token limits
- Prioritize recent messages for context

## Security Considerations

### Agent Safety
- Validate all tool calls before execution
- Implement proper error handling to prevent agent loops
- Sanitize user input to prevent prompt injection

### MCP Tool Security
- All MCP tools already validate user_id (built in Module 2)
- No additional security measures needed beyond existing implementation
- Agent operates with same authorization constraints as direct API calls

## Technology Stack Alignment

### Dependencies
- `openai` Python SDK for Assistant API integration
- Existing `mcp` SDK for MCP server communication
- Existing `sqlmodel` and `fastapi` for backend integration
- No new major dependencies beyond what's already in the ecosystem

### Performance Requirements
- Target response time < 10 seconds (as specified in NFR-001)
- Optimize database queries with proper indexing
- Consider async processing for long-running operations

## Implementation Risks

### High-Risk Areas
1. **OpenAI API availability**: Implement fallback/error handling for API outages
2. **MCP server connectivity**: Ensure robust connection handling between services
3. **Database performance**: Optimize queries for conversation history loading
4. **Token consumption**: Monitor and optimize context window usage

### Mitigation Strategies
1. Implement circuit breaker pattern for external API calls
2. Add comprehensive monitoring and alerting
3. Use connection pooling for database operations
4. Implement caching for frequently accessed data

## Research Conclusion

All technical unknowns have been addressed through research. The implementation approach leverages existing components (MCP server, JWT auth, SQLModel) while integrating OpenAI's Assistant API for the conversational interface. The design satisfies all constitutional requirements including stateless operation, security, and persistence.