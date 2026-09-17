from typing import Literal
from pydantic import BaseModel, Field, HttpUrl

Auth = Literal['oauth2','api_key','basic','token','other','unknown']
Access = Literal['self_serve_free','self_serve_trial','paid_plan_required','admin_approval','partner_gated','enterprise_only','no_public_api','unknown']
ApiStyle = Literal['rest','graphql','soap','local_cli','none','unknown']
Breadth = Literal['broad','narrow','none','unknown']
Verdict = Literal['yes','partial','no']
Blocker = Literal['none','paid_tier','partner_review','app_review','enterprise_only','no_api','unstable_api','unknown']

class SourceCapture(BaseModel):
    requested_url: str
    resolved_url: str | None = None
    status: int
    title: str = ''
    excerpt: str = ''
    retrieved_at: str
    error: str | None = None

class Evidence(BaseModel):
    field: Literal['auth','access','api_surface','mcp','buildability']
    url: str
    quote: str
    source_title: str = ''
    retrieved_at: str

class AppResult(BaseModel):
    id: int
    name: str
    category: str
    one_liner: str
    auth_methods: list[Auth]
    access: Access
    auth_primary: Auth
    api_style: list[ApiStyle]
    api_breadth: Breadth
    official_mcp: bool
    mcp_status: Literal['official','community','unconfirmed','none']
    buildable: Verdict
    blocker: str | None = None
    blocker_class: Blocker = 'unknown'
    evidence_url: str
    evidence_note: str
    confidence: float = Field(ge=0, le=1)
    pass_reached: int = Field(ge=1, le=3)
    source_capture: SourceCapture | None = None
    evidence: list[Evidence] = []
