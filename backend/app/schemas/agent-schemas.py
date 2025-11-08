from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class TextIn(BaseModel):
    text: str
    user_id: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

class IntentOut(BaseModel):
    intent: str
    confidence: float = 0.75

class CopyIn(BaseModel):
    brief: str
    tone: Optional[str] = Field(default="neutraalne")
    length: Optional[str] = Field(default="lühike")

class CopyOut(BaseModel):
    content: str

class CalendarIn(BaseModel):
    utterance: str
    user_id: Optional[str] = None

class CalendarOut(BaseModel):
    action: str
    when: Optional[str] = None
    title: Optional[str] = None
    location: Optional[str] = None

class FAQIn(BaseModel):
    question: str

class FAQOut(BaseModel):
    answer: str
    matched_q: Optional[str] = None
    score: float

class AnalyticsIn(BaseModel):
    events: List[Dict[str, Any]]

class AnalyticsOut(BaseModel):
    summary: str

class ContextGetIn(BaseModel):
    user_id: str

class ContextUpdateIn(BaseModel):
    user_id: str
    kv: Dict[str, Any]

class PricingItem(BaseModel):
    name: str
    qty: float = 1
    unit_price: float

class PricingIn(BaseModel):
    items: List[PricingItem]
    discount_pct: float = 0
    vat_pct: float = 22

class PricingOut(BaseModel):
    subtotal: float
    discount: float
    vat: float
    total: float
    breakdown: List[Dict[str, Any]]

class SentimentOut(BaseModel):
    label: str
    confidence: float

class EscalateIn(BaseModel):
    message: str
    sentiment: Optional[SentimentOut] = None

class EscalateOut(BaseModel):
    escalate: bool
    reason: str

class FollowupIn(BaseModel):
    conversation_summary: str

class FollowupOut(BaseModel):
    message: str

