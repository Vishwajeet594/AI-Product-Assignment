from typing import Literal
from pydantic import BaseModel, Field, HttpUrl

Auth = Literal['oauth2','api_key','basic','token','other','unknown']
Access = Literal['self_serve_free','self_serve_trial','paid_plan_required','admin_approval','partner_gated','no_public_api','unknown']

class AppResult(BaseModel):
    id: int
    name: str
    category: str
    one_liner: str
    auth_methods: list[Auth]
    access: Access
    api_style: list[Literal['rest','graphql','soap','local_cli','none','unknown']]
    api_breadth: Literal['broad','narrow','none','unknown']
    official_mcp: bool
    buildable: Literal['yes','partial','no']
    blocker: str | None = None
    blocker_class: Literal['none','paid_tier','partner_review','app_review','enterprise_only','no_api','unstable_api','unknown'] = 'unknown'
    evidence_url: str
    evidence_note: str
    confidence: float = Field(ge=0, le=1)
    pass_reached: int = Field(ge=1, le=3)
