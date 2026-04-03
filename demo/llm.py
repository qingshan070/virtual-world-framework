import json
from .types import LLMActionOutput, DecisionType, EmotionType, OpenEvent, StressType, ResourceDim
import os
from typing import Dict, Any, Optional

class ConsistencyValidator:
    """验证 LLM 输出是否符合物理与心理法则"""
    @staticmethod
    def validate(llm_output: LLMActionOutput, context: Dict[str, Any]) -> bool:
        sensation = context.get("sensation", 0.0)
        phase = context.get("phase", "PEARLITE")
        is_yielded = context.get("is_yielded", False)
        
        # 极度痛苦时不能开心 (除非是疯了/马氏体/渗碳体)
        if sensation < -0.5 and phase in ["PEARLITE", "AUSTENITE"]:
            if llm_output.emotion in [EmotionType.GRATEFUL, EmotionType.HOPEFUL, EmotionType.JOY]:
                return False
                
        # Issue 10.3: 增强物理一致性约束，防止 LLM 严重漂移
        # 1. 断裂态必须崩溃
        if phase == "FRACTURE":
            if llm_output.decision_type != DecisionType.BREAKDOWN:
                return False
                
        # 2. 圣化态 (奥氏体) 极难发生报复性爆发
        if phase == "AUSTENITE" and llm_output.decision_type == DecisionType.EXPLODE:
            # 除非是极端的“牺牲式爆发”，否则拦截至 ACT
            pass 
            
        # 3. 合金注入合法性
        if llm_output.alloy_injection:
            if not llm_output.alloy_injection.reason:
                return False
                
        return True

class LLMWithFallback:
    """LLM Parser with Graceful Degradation: 带有优雅降级机制的 LLM 解析器
    
    在没有配置 API Key 或未安装 litellm 时，将平滑降级到纯数学推演或基础事件模式。
    """
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model = model_name
        self.validator = ConsistencyValidator()
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.completion_func = None
        
        if self.api_key:
            try:
                from litellm import completion
                self.completion_func = completion
            except ImportError:
                print("  [警告] 未安装 litellm 依赖，LLM 解析功能将被禁用，自动降级为纯数学模式。")
                self.api_key = "" # 强制禁用
        
    def generate_action(self, prompt: str, allow_injection: bool = False, context: Dict[str, Any] = None) -> Optional[LLMActionOutput]:
        """调用 LLM 并尝试解析结构化输出"""
        if not self.api_key:
            return None
            
        injection_schema = ""
        if allow_injection:
            injection_schema = """,
    "alloy_injection": {
        "element": "C|S|Cr|Ni|P|Mn",
        "concentration": 0.05,
        "reason": "..."
    }"""
            
        json_schema_prompt = f'''
请严格输出 JSON 格式:
{{
    "decision_type": "EXPLODE|ACT|HESITATE|SUPPRESS|BREAKDOWN",
    "emotion": "NEUTRAL|FEAR|ANGER|SADNESS|JOY|HOPEFUL|GRATEFUL|DESPAIR|COLD|MANIC|HOLLOW",
    "action_description": "...",
    "inner_monologue": "...",
    "body_language": "..."{injection_schema}
}}'''

        messages = [
            {"role": "system", "content": "你是一个运行在虚拟世界基础设施(VWI)上的核心解析器。你的任务是将自然语言描述的事件或角色的微观心理状态映射为严格的 JSON 结构。\n" + json_schema_prompt},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.completion_func(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            result_str = response.choices[0].message.content
            data = json.loads(result_str)
            
            output = LLMActionOutput(**data)
            
            # 物理一致性校验
            if context and not self.validator.validate(output, context):
                print("  [LLM 拦截] 输出违反了物理或心理一致性法则。")
                return None
                
            return output
            
        except Exception as e:
            print(f"  [LLM 失败] 解析错误: {str(e)}")
            return None

    def parse_event(self, text: str, context: str) -> OpenEvent:
        """造物主模式下将自然语言转换为张量事件"""
        if not self.api_key:
            # Fallback
            return OpenEvent(
                id="evt_manual_fallback",
                description=text,
                impact_vector={ResourceDim.SOMATIC: -0.1},
                stress_type=StressType.SHEAR
            )
            
        prompt = f"""
请将以下自然语言事件描述转化为张量冲击。
背景：{context}
事件描述："{text}"

输出 JSON 格式：
{{
    "description": "精炼后的事件描述",
    "impact_vector": {{
        "SOMATIC": float, // 肉体伤害或治愈 [-1.0, 1.0]
        "MATERIAL": float, // 财富得失
        "SOCIAL": float, // 权力或名誉得失
        "IDEOLOGICAL": float // 精神打击或鼓舞
    }},
    "stress_type": "COMPRESSIVE|TENSILE|SHEAR|CORROSION"
}}
        """
        
        try:
            response = self.completion_func(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个事件张量解析器。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            return OpenEvent(
                id="evt_llm_" + str(hash(text))[:8],
                description=data["description"],
                impact_vector={ResourceDim(k): v for k, v in data["impact_vector"].items()},
                stress_type=StressType(data["stress_type"])
            )
        except Exception as e:
            print(f"[LLM 失败] {e}")
            return OpenEvent(
                id="evt_manual_fallback",
                description=text,
                impact_vector={ResourceDim.SOMATIC: -0.1},
                stress_type=StressType.SHEAR
            )