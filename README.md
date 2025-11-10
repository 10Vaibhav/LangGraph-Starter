# LangGraph-Starter

A collection of LangGraph examples demonstrating core concepts like state management, node composition, conditional routing, and persistent conversation memory with multiple LLM providers.

## Overview

This repository contains practical examples to help you get started with LangGraph, a framework for building stateful, multi-actor applications with LLMs. Learn how to build basic graph flows, implement smart routing with conditional edges, and create chatbots with persistent memory using MongoDB checkpointing.

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.