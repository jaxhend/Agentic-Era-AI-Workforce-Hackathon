from fastapi import APIRouter
from backend.app.schemas.schemas import TextIn
from ..agents import router_agent as agent

router = APIRouter(prefix="/router", tags=["router"])

@router.post("/route")
async def route_query(body: TextIn):
    """
    Receives a user query and routes it to the appropriate agent.
    """
    return await agent.route(body.text)
from ..services import llm_client
import json

# This prompt is the "brain" of the router agent.
# It lists all available tools (agents) and instructs the LLM on how to choose one.
TEMPLATE = """
You are an intelligent routing agent. Your task is to analyze the user's query and determine which API endpoint (agent) should be called to handle it.
You must return a single, valid JSON object containing "endpoint" and "payload" keys.

Here are the available agents and their descriptions:

- endpoint: "/intent/analyze"
  - description: "Classifies a short user text into a single category like 'booking', 'question', 'complaint', 'thanks', 'offer', 'price inquiry'."
  - payload: {"text": "The user's original text."}
  - example_query: "I want to complain."

- endpoint: "/copywriter/generate"
  - description: "Generates a longer text in Estonian based on a creative brief, a specific tone, and desired length."
  - payload: {"brief": "The user's creative brief.", "tone": "neutral", "length": "short"}
  - example_query: "Write me a short and neutral ad copy about a new coffee shop."

- endpoint: "/calendar/interpret"
  - description: "Parses a user's natural language command related to scheduling, such as adding, updating, or querying calendar events."
  - payload: {"utterance": "The user's full command about the event."}
  - example_query: "Book a meeting for tomorrow at 10 AM with John."

- endpoint: "/faq/answer"
  - description: "Answers a user's question by finding the best match from a list of frequently asked questions (FAQs). Use for general questions about products, services, or policies."
  - payload: {"question": "The user's question."}
  - example_query: "What is the delivery time?"

- endpoint: "/pricing/quote"
  - description: "Calculates a price quote based on a list of items, quantities, and discounts. The query must contain structured item information."
  - payload: {"items": [{"name": "item_name", "qty": 1, "unit_price": 10.0}], "discount_pct": 0, "vat_pct": 22}
  - example_query: "Calculate the price for 2 units of 'Product A' at 50 EUR each with a 10% discount."

- endpoint: "/sentiment/analyze"
  - description: "Analyzes the emotional tone (sentiment) of a given text, classifying it as 'positive', 'neutral', or 'negative'."
  - payload: {"text": "The user's text to be analyzed."}
  - example_query: "I am very unhappy with your service."

- endpoint: "/escalate/check"
  - description: "Checks if a conversation needs to be escalated to a human agent based on negative sentiment or sensitive keywords."
  - payload: {"message": "The user's message that might require escalation."}
  - example_query: "This is not working and I want a refund."

- endpoint: "/followup/generate"
  - description: "Generates a professional follow-up message based on a summary of a conversation."
  - payload: {"conversation_summary": "A brief summary of the past conversation."}
  - example_query: "Summarize our chat and write a follow-up email."

- endpoint: "/router/route"
  - description: "This is you! Do not choose this endpoint. If no other agent is suitable, return an error."
  - payload: {}
  - example_query: ""

If no agent is suitable for the user's query, return a JSON object with endpoint set to "none" and a "reason" in the payload.

User Query:
{query}

JSON Response:
"""

async def route(query: str) -> dict:
    """
    Uses an LLM to decide which agent to call based on the user's query.
    """
    prompt = TEMPLATE.format(query=query)
    # We ask for a slightly larger response to accommodate complex payloads
    raw_response = await llm_client.complete(prompt, max_tokens=300)

    # Clean up the response to ensure it's valid JSON
    raw_response = raw_response.strip().strip('`')
    if raw_response.startswith("json"):
        raw_response = raw_response[4:].strip()

    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        # If the LLM fails to return valid JSON, we return a default error state
        return {
            "endpoint": "none",
            "payload": {"reason": "Failed to determine a valid route for the query."}
        }

