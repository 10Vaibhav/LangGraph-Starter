# LangGraph-Starter

A collection of LangGraph examples demonstrating core concepts like state management, node composition, conditional routing, and persistent conversation memory with multiple LLM providers.

## Overview

This repository contains practical examples to help you get started with LangGraph, a framework for building stateful, multi-actor applications with LLMs. Learn how to build basic graph flows, implement smart routing with conditional edges, and create chatbots with persistent memory using MongoDB checkpointing.

## Prerequisites

- Python 3.8+
- Docker (for MongoDB, Qdrant, and Neo4j)
- OpenAI API key
- Google Gemini API key (for conditional routing example)

## Examples

### 1. LangGraph_Learnings.py - Basic Graph Flow

A foundational example demonstrating:
- **State Management**: Using `TypedDict` with `add_messages` annotation for message accumulation
- **Sequential Node Execution**: Building a simple linear graph flow
- **Message Handling**: How LangGraph appends messages rather than replacing them

**Key Concepts:**
```python
# Messages are accumulated, not replaced
# Initial: {"messages": ["Hi, My name is Vaibhav Mahajan"]}
# After chatbot: {"messages": ["Hi, My name is Vaibhav Mahajan", "LLM Response"]}
# After sampleNode: {"messages": [...previous messages..., "Sample Message Appended"]}
```

**Graph Flow:**
![LangGraph Flow Diagram](./Simple_LangGraph_Flow_Diagram.png)


### 2. Conditional_Edges_Smart_Routing.py - Smart Routing with Evaluation

An advanced example showcasing:
- **Conditional Edges**: Dynamic routing based on response evaluation
- **Multi-LLM Integration**: Using both OpenAI (GPT-4) and Google Gemini
- **Quality Control**: Automatic response evaluation and fallback mechanism
- **Smart Routing**: Routes to Gemini if OpenAI response is unsatisfactory

**Graph Flow:**
![LangGraph Conditional Edges Smart Routing Flow Diagram](./LangGraph._Flow_Diagram_Conditional_Edges.png)


### 3. LangGraph_Checkpoint.py - Persistent Conversation Memory

A stateful chatbot example demonstrating:
- **MongoDB Checkpointing**: Persists conversation history across sessions
- **Thread-based Memory**: Uses thread IDs to maintain separate conversation contexts
- **Session Continuity**: Resume conversations from where you left off
- **Streaming Responses**: Real-time message display

**Key Features:**
```python
# Conversations are stored in MongoDB with thread_id
config = {"configurable": {"thread_id": "user_123"}}
# Same thread_id retrieves previous conversation history
```

**Use Case:** Build chatbots that remember user context across multiple sessions, enabling personalized and continuous interactions.

### 4. memory_agent - Semantic Memory with Mem0

A practical implementation of semantic memory using Mem0 with support for both Qdrant vector database and Neo4j graph database:
- **Persistent User Memory**: Stores and retrieves user-specific context across conversations
- **Vector Search**: Uses embeddings to find relevant memories semantically
- **Multi-layered Memory**: Supports different memory types (user, session, agent)
- **Dual Storage Options**: 
  - **Qdrant**: Fast vector similarity search with local deployment
  - **Neo4j**: Graph-based memory storage for relationship-aware context

**Key Features:**
```python
# Store memories with user context
mem_client.add(user_id="user_123", messages=[...])

# Semantic search through memories
memories = mem_client.search(query="user query", user_id="user_123")

# Inject relevant memories into LLM context
SYSTEM_PROMPT = f"Context: {json.dumps(memories)}"
```

**Memory Types:**
![Types of Memory](./memory_agent/Types_of_Memory.png)

**Neo4j Graph Visualization:**
![Neo4j Graph Visualization](./memory_agent/Neo4j_Graph_visualisation.png)

**Architecture:**
- Mem0 for memory management
- OpenAI embeddings (text-embedding-3-small)
- Storage options:
  - Qdrant vector database for semantic search
  - Neo4j graph database for relationship-based memory
- GPT-4 for response generation

**Neo4j Integration:**
Neo4j provides a graph-based approach to memory storage, enabling:
- **Relationship Mapping**: Connect memories based on entities, topics, and context
- **Graph Queries**: Traverse memory relationships for deeper context understanding
- **Visual Exploration**: Visualize memory connections and patterns
- **Complex Queries**: Use Cypher query language for advanced memory retrieval

Learn more about Neo4j: [Neo4j Getting Started Guide](https://neo4j.com/docs/getting-started/)

**Use Case:** Build AI agents that remember user preferences, past interactions, and context, enabling truly personalized conversations that improve over time. Use Neo4j when you need to understand relationships between memories and entities.

## Key LangGraph Concepts

### State Management
- Use `TypedDict` to define your graph state
- `Annotated[list, add_messages]` enables message accumulation
- State flows through nodes and gets updated

### Nodes
- Functions that process state and return updates
- Can call LLMs, APIs, or perform any logic
- Return dictionaries that merge into the state

### Edges
- **Regular Edges**: Direct connections between nodes
- **Conditional Edges**: Dynamic routing based on state or logic
- Use `Literal` types to define possible routing destinations

### Graph Building
```python
graph_builder = StateGraph(State)
graph_builder.add_node("node_name", node_function)
graph_builder.add_edge(START, "first_node")
graph_builder.add_conditional_edges("node", routing_function)
graph = graph_builder.compile()
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with API keys:
```
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_gemini_key
DB_URL=mongodb://admin:admin@localhost:27017
```

3. Start required services:
```bash
# For LangGraph_Checkpoint.py
docker-compose up -d

# For memory_agent
cd memory_agent
docker-compose up -d
```

## Resources

- [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph/overview) - Official LangGraph documentation and guides
- [Mem0 Dashboard](https://app.mem0.ai/dashboard/get-started) - Get started with Mem0 for memory management

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.