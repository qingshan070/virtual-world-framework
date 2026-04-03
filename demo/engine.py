import os
import json
import random
from typing import List, Optional, Any
from .vessel import VesselEngine
from .sentient import SentientEngine
from .types import OpenEvent, StressType, ResourceDim, InteractionMode

class SimulationEngine:
    def __init__(self, use_llm: bool = False, model_name: str = "gpt-3.5-turbo", mode: InteractionMode = InteractionMode.GOD, avatar_id: str = None, population: int = 4, seed: Optional[int] = None):
        
        # Issue 10.1: 增加随机数种子，保证基础物理与角色生成的可复现性
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            
        self.vessel = VesselEngine(region_id="R01")
        self.sentient = SentientEngine(use_llm=use_llm, model_name=model_name, population=population)
        from .llm import LLMWithFallback
        self.llm_parser = LLMWithFallback(model_name=model_name) if use_llm else None
        self.tick_count = 0
        self.log_file = "outputs/run_log.jsonl"
        os.makedirs("outputs", exist_ok=True)
        self.mode = mode
        self.avatar_id = avatar_id # 仅在 AVATAR 模式下使用
        self.pending_writebacks = []
        
    def run(self, ticks: int = 10, interactive: bool = False):
        print(f"=== V10.0 无限沙盒 | 模式={self.mode.value} | LLM={self.sentient.use_llm} ===")
        if self.mode == InteractionMode.GOD:
            print("造物主模式：你可以输入任何自然语言，LLM将自动翻译为四大维度的张量冲击。")
        elif self.mode == InteractionMode.ARCHON:
            print("执政官模式：你只能通过输入 'tax' (加税), 'relief' (赈灾), 'exam' (开科取士) 等宏观政策来调控世界。")
        elif self.mode == InteractionMode.AVATAR:
            print(f"凡人降临模式：你现在是 [{self.sentient.characters.get(self.avatar_id).name if self.avatar_id in self.sentient.characters else '未知'}]。你只能对你认识的人做出反应。")
            
        for t in range(ticks):
            self.tick_count += 1
            
            creator_events = []
            if interactive:
                prompt_msg = f"\n[Tick {self.tick_count}] 请输入指令 (输入'q'退出): "
                user_input = input(prompt_msg).strip()
                
                if user_input.lower() == 'q':
                    break
                    
                if user_input:
                    if self.mode == InteractionMode.GOD:
                        if self.llm_parser:
                            world_context = f"当前环境冲突度: {self.vessel.conflict_level:.1f}，资源存量: 肉体={self.vessel.resources[ResourceDim.SOMATIC]:.1f}"
                            parsed_event = self.llm_parser.parse_event(user_input, world_context)
                            creator_events.append(parsed_event)
                        else:
                            print("  [警告] 未开启 LLM，无法解析自然语言事件，已忽略。")
                            
                    elif self.mode == InteractionMode.ARCHON:
                         if user_input == "tax":
                             creator_events.append(OpenEvent(id=f"evt_cmd_{self.tick_count}", description="执政官下令横征暴敛，增加赋税！", impact_vector={ResourceDim.MATERIAL: -1.0, ResourceDim.SOCIAL: -0.5}, stress_type=StressType.COMPRESSIVE))
                         elif user_input == "relief":
                             creator_events.append(OpenEvent(id=f"evt_cmd_{self.tick_count}", description="执政官下令开仓放粮，赈济灾民。", impact_vector={ResourceDim.SOMATIC: 0.5, ResourceDim.MATERIAL: 0.5}, stress_type=StressType.TENSILE))
                         elif user_input == "exam":
                             creator_events.append(OpenEvent(id=f"evt_cmd_{self.tick_count}", description="执政官宣布开科取士，提供晋升通道。", impact_vector={ResourceDim.SOCIAL: 0.8, ResourceDim.IDEOLOGICAL: 0.5}, stress_type=StressType.TENSILE))
                         else:
                             print("  [警告] 未知的执政官指令。")
                             
                    elif self.mode == InteractionMode.AVATAR:
                        if self.llm_parser and self.avatar_id:
                             world_context = "你正在解析一个玩家扮演的角色的微观行为。"
                             parsed_event = self.llm_parser.parse_event(user_input, world_context)
                             parsed_event.source_entity_id = self.avatar_id # 绑定源头为玩家角色
                             creator_events.append(parsed_event)
                        else:
                             print("  [警告] 未开启 LLM，无法解析自然语言事件，已忽略。")
            
            # 1. 物理世界自然演化
            vessel_events = self.vessel.process_tick(self.pending_writebacks)
            
            # 2. 合并事件
            all_events = vessel_events + creator_events
            
            if all_events:
                 print(f"\n[Tick {self.tick_count}] *** 物理世界发生事件 ***")
                 for ev in all_events:
                    print(f"  !! {ev.description} (主应力:{ev.stress_type.value})")
            elif self.tick_count % 5 == 0:
                 print(f"\n[Tick {self.tick_count}] (世界平静地运转着...)")

            # 3. 心理世界感知事件
            self.pending_writebacks = self.sentient.process_tick(all_events, self.tick_count)
                
            # 打印有情世间状态
            if all_events or self.tick_count % 5 == 0:
                 for char_id, char in self.sentient.characters.items():
                    # AVATAR 模式下，只打印玩家角色和与其相关的事件反馈
                    if self.mode == InteractionMode.AVATAR and char_id != self.avatar_id:
                        continue
                        
                    mat = char.material
                    print(f"  [{char.name}] 相态:{mat.phase.value} | 刚度:{mat.stiffness:.1f} | 扭曲度:{mat.plastic_strain:.2f}")
                    wb = next((w for w in self.pending_writebacks if w.entity_id == char_id), None)
                    if wb:
                        print(f"    -> {wb.narrative_log}")
                        if wb.triggered_phase_event:
                            print(f"    -> [相变广播] {wb.triggered_phase_event}")
                    elif all_events:
                        print(f"    -> [内心毫无波澜，直接免疫了该事件的伤害]")
            
            # 4. 保存快照
            self._dump_log(all_events, self.pending_writebacks)
            
    def _dump_log(self, events: List[Any], writebacks: List[Any]):
        state = {
            "tick": self.tick_count,
            "vessel": {
                "resources": {k.value: v for k, v in self.vessel.resources.items()},
                "conflict": self.vessel.conflict_level
            },
            "events": [e.model_dump() for e in events],
            "writebacks": [w.model_dump() for w in writebacks],
            "sentient": {
                cid: {
                    "phase": c.material.phase.value,
                    "stiffness": c.material.stiffness,
                    "toughness": c.material.toughness,
                    "plastic_strain": c.material.plastic_strain,
                    "elements": c.material.elements,
                    "expected_resources": {k.value: v for k, v in c.expected_resources.items()}
                } for cid, c in self.sentient.characters.items()
            }
        }
        
        mode = "a" if self.tick_count > 1 else "w"
        with open(self.log_file, mode, encoding="utf-8") as f:
            f.write(json.dumps(state, ensure_ascii=False) + "\n")