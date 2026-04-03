from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class ResourceDim(str, Enum):
    SOMATIC = "SOMATIC"         # 肉体/生存
    MATERIAL = "MATERIAL"       # 物质/财富
    SOCIAL = "SOCIAL"           # 社会/权力
    IDEOLOGICAL = "IDEOLOGICAL" # 精神/信仰

class StressType(str, Enum):
    COMPRESSIVE = "COMPRESSIVE" # 压缩应力 (如饥荒、贫穷)
    TENSILE = "TENSILE"         # 拉伸应力 (如暴富、溺爱)
    SHEAR = "SHEAR"             # 剪切应力 (如战乱、背叛)
    CORROSION = "CORROSION"     # 腐蚀应力 (如瘟疫、谣言)

class PhaseType(str, Enum):
    PEARLITE = "PEARLITE"       # 珠光体 (常态：软硬适中)
    MARTENSITE = "MARTENSITE"   # 马氏体 (黑化：极硬、极脆、丧失同理心)
    AUSTENITE = "AUSTENITE"     # 奥氏体 (圣徒：极软、极韧、包容一切)
    CEMENTITE = "CEMENTITE"     # 渗碳体 (异化：极硬但自私，暴发户心态)
    FRACTURE = "FRACTURE"       # 断裂态 (彻底崩溃、疯狂)

class DecisionType(str, Enum):
    EXPLODE = "EXPLODE"
    ACT = "ACT"
    HESITATE = "HESITATE"
    SUPPRESS = "SUPPRESS"
    BREAKDOWN = "BREAKDOWN"

class EmotionType(str, Enum):
    NEUTRAL = "NEUTRAL"
    FEAR = "FEAR"
    ANGER = "ANGER"
    SADNESS = "SADNESS"
    JOY = "JOY"
    HOPEFUL = "HOPEFUL"
    GRATEFUL = "GRATEFUL"
    DESPAIR = "DESPAIR"
    COLD = "COLD"
    MANIC = "MANIC"
    HOLLOW = "HOLLOW"

class InteractionMode(str, Enum):
    GOD = "GOD"
    ARCHON = "ARCHON"
    AVATAR = "AVATAR"

# ====================
# Data Models
# ====================

class PhysicalStress(BaseModel):
    type: StressType
    intensity: float = Field(..., description="[0, 1]")
    source_event_id: str
    description: str

class OpenEvent(BaseModel):
    id: str
    description: str
    impact_vector: Dict[ResourceDim, float]
    stress_type: StressType
    source_entity_id: Optional[str] = None # 事件发起者

class EpisodicMemory(BaseModel):
    tick: int
    description: str
    salience: float = 0.0

class AlloyInjection(BaseModel):
    element: str # C, S, Cr, Ni, P, Mn
    concentration: float
    reason: str

class LLMActionOutput(BaseModel):
    decision_type: DecisionType
    emotion: EmotionType
    action_description: str
    inner_monologue: str
    body_language: str
    alloy_injection: Optional[AlloyInjection] = None

class MaterialState(BaseModel):
    stiffness: float = 1.0     # E
    toughness: float = 1.0     # T
    yield_point: float = 0.8   # σ_y
    break_point: float = 1.5   # σ_f
    plastic_strain: float = 0.0 # ε_p
    phase: PhaseType = PhaseType.PEARLITE
    elements: Dict[str, float] = Field(default_factory=dict)

class Relationship(BaseModel):
    target_id: str
    intimacy: float = 0.5
    trust: float = 0.5
    distance: float = 1.0
    entity_memories: List[str] = Field(default_factory=list)

class CharacterPersonality(BaseModel):
    openness: float = 0.5
    conscientiousness: float = 0.5
    extraversion: float = 0.5
    agreeableness: float = 0.5
    neuroticism: float = 0.5

class CharacterState(BaseModel):
    id: str
    name: str
    age: int
    desire_matrix: Dict[ResourceDim, float]
    expected_resources: Dict[ResourceDim, float]
    material: MaterialState
    personality: CharacterPersonality
    sensation: float = 0.0
    relationships: Dict[str, Relationship] = Field(default_factory=dict)
    episodic_memories: List[EpisodicMemory] = Field(default_factory=list)
    memory_summary: str = "一个普通的虚拟世界居民。"

class KarmaWriteback(BaseModel):
    entity_id: str
    decision: DecisionType
    resource_deltas: Dict[ResourceDim, float] = Field(default_factory=lambda: {d: 0.0 for d in ResourceDim})
    conflict_delta: float = 0.0
    cooperation_delta: float = 0.0
    narrative_log: str
    triggered_phase_event: Optional[str] = None