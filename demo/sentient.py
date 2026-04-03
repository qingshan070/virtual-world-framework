from typing import List, Dict, Optional, Any
from .types import CharacterState, OpenEvent, PhysicalStress, ResourceDim, PhaseType, DecisionType, KarmaWriteback, MaterialState, CharacterPersonality, Relationship, EpisodicMemory, StressType
from .material import MaterialPhysics
from .llm import LLMWithFallback

class SentientEngine:
    """有情世间引擎 (V10.0): 负责角色的七步演算与相变触发"""
    
    def __init__(self, use_llm: bool = False, model_name: str = "gpt-3.5-turbo", population: int = 4):
        self.characters: Dict[str, CharacterState] = {}
        self.use_llm = use_llm
        self.llm_engine = LLMWithFallback(model_name=model_name) if use_llm else None
        
        # 初始化随机人口 (无剧本)
        self._init_random_population(population)
        
    def _init_random_population(self, population: int):
        import random
        names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        
        for i in range(population):
            char_id = f"char_{i}"
            name = f"Node_{names[i % len(names)]}_{i}"
            
            # 随机生成执念矩阵 (Desire Matrix)
            desires = {
                ResourceDim.SOMATIC: random.uniform(0.1, 0.9),
                ResourceDim.MATERIAL: random.uniform(0.1, 0.9),
                ResourceDim.SOCIAL: random.uniform(0.1, 0.9),
                ResourceDim.IDEOLOGICAL: random.uniform(0.1, 0.9)
            }
            
            # 随机生成初始期望
            expectations = {
                ResourceDim.SOMATIC: random.uniform(10.0, 100.0),
                ResourceDim.MATERIAL: random.uniform(10.0, 100.0),
                ResourceDim.SOCIAL: random.uniform(10.0, 100.0),
                ResourceDim.IDEOLOGICAL: random.uniform(10.0, 100.0)
            }
            
            # 随机初始材质 (常态珠光体，刚度和韧性各有侧重)
            mat = MaterialState(
                stiffness=random.uniform(0.5, 2.5),
                toughness=random.uniform(0.5, 2.5),
                yield_point=random.uniform(0.6, 1.2),
                phase=PhaseType.PEARLITE
            )
            
            self.characters[char_id] = CharacterState(
                id=char_id,
                name=name,
                age=random.randint(18, 60),
                desire_matrix=desires,
                expected_resources=expectations,
                material=mat,
                personality=CharacterPersonality(),
                memory_summary=f"初始生成的虚拟节点，拥有随机的材质和执念。"
            )
            
        # 建立 V0 随机拓扑图谱
        char_ids = list(self.characters.keys())
        for i, cid1 in enumerate(char_ids):
            for j, cid2 in enumerate(char_ids):
                if i != j:
                    # 建立基础连接
                    self.characters[cid1].relationships[cid2] = Relationship(
                        target_id=cid2,
                        trust=random.uniform(0.0, 1.0),
                        distance=random.uniform(1.0, 5.0)
                    )
        
    def process_tick(self, events: List[OpenEvent], tick_count: int) -> List[KarmaWriteback]:
        """演化一个 Tick，所有角色并发处理感知与决策"""
        writebacks = []
        
        # 1. 记忆与期望随时间衰减
        for char in self.characters.values():
            char.episodic_memories = [m for m in char.episodic_memories if m.salience > 0.1]
            for m in char.episodic_memories:
                m.salience *= 0.95 # 记忆衰减
                
        # 2. 处理事件
        new_social_events = [] # 角色行为产生的次生事件
        for event in events:
            source_entity_id = getattr(event, "source_entity_id", None)
            
            for char_id, char in self.characters.items():
                # 衰减计算
                attenuation = 1.0
                if source_entity_id and source_entity_id != char_id:
                    # 获取角色与事件源的关系
                    rel = char.relationships.get(source_entity_id)
                    if rel:
                        # 距离越远，冲击越小；信任度越低，冲击越小（不信谣言）
                        attenuation = rel.trust / max(1.0, rel.distance)
                    else:
                        # 陌生人事件衰减极大
                        attenuation = 0.1
                        
                # 如果衰减后影响太小，忽略
                if attenuation < 0.05:
                    continue
                    
                # 应用衰减
                attenuated_event = event.model_copy(deep=True)
                for dim in attenuated_event.impact_vector:
                    attenuated_event.impact_vector[dim] *= attenuation
                    
                # 在衰减后计算物理应力张量
                max_impact = max([abs(v) for v in attenuated_event.impact_vector.values() if v < 0] + [0.0])
                stress = PhysicalStress(
                    type=attenuated_event.stress_type,
                    intensity=max_impact,
                    source_event_id=attenuated_event.id,
                    description=attenuated_event.description
                )
                
                wb = self._process_character(char, attenuated_event, stress, tick_count)
                if wb:
                    writebacks.append(wb)
                    # 角色极端的决定（如爆发）会作为新的社交事件广播
                    if wb.decision == DecisionType.EXPLODE:
                        new_social_events.append(OpenEvent(
                            id=f"evt_soc_{char_id}_{tick_count}",
                            description=f"{char.name} 陷入疯狂，产生极端的爆发行为！",
                            impact_vector={ResourceDim.SOMATIC: -0.5, ResourceDim.SOCIAL: -0.2},
                            stress_type=StressType.SHEAR,
                            source_entity_id=char_id # 记录源头
                        ))
                        
        # 简单的次生事件处理 (只处理一层，避免无限递归)
        if new_social_events:
            for event in new_social_events:
                source_entity_id = getattr(event, "source_entity_id", None)
                for char_id, char in self.characters.items():
                    if char_id == source_entity_id: continue
                    attenuation = 0.1
                    rel = char.relationships.get(source_entity_id)
                    if rel: attenuation = rel.trust / max(1.0, rel.distance)
                    if attenuation < 0.05: continue
                    attenuated_event = event.model_copy(deep=True)
                    for dim in attenuated_event.impact_vector: attenuated_event.impact_vector[dim] *= attenuation
                    
                    max_impact = max([abs(v) for v in attenuated_event.impact_vector.values() if v < 0] + [0.0])
                    stress = PhysicalStress(type=attenuated_event.stress_type, intensity=max_impact, source_event_id=attenuated_event.id, description=attenuated_event.description)
                    
                    wb = self._process_character(char, attenuated_event, stress, tick_count)
                    if wb: writebacks.append(wb)
                    
        return writebacks

    def _process_character(self, char: CharacterState, event: OpenEvent, stress: PhysicalStress, tick_count: int) -> KarmaWriteback:
        """核心管线：触缘受想行识业 (V10.0)"""
        
        # 修复缺陷一：碎裂后的“活死人”悖论
        if char.material.phase == PhaseType.FRACTURE:
            # 彻底碎裂的疯子不再进行理性的应力计算，直接输出混乱行为
            return self._generate_karma(char, DecisionType.BREAKDOWN, "[断裂态] 丧失理智，陷入彻底的疯狂与混乱。", None)
            
        # --- Step 1 & 2: 触、缘 (多维主观应力计算) ---
        total_subjective_stress = 0.0
        total_tensile_stress = 0.0
        
        for dim, impact in event.impact_vector.items():
            desire = char.desire_matrix.get(dim, 0.0)
            # 只有他在乎这个维度(desire>0)，冲击才会转化为痛感
            if impact < 0:
                total_subjective_stress += abs(impact) * desire
            else:
                total_tensile_stress += impact * desire
                
            # Hedonic Adaptation (享乐适应): 期望会随着近期受到的冲击而逐渐发生偏移
            char.expected_resources[dim] += 0.1 * impact
            
        # 情境与关系放大 (如果事件来自于一个非常信任的人的背叛，应力激增)
        source_id = getattr(event, "source_entity_id", None)
        if source_id and source_id in char.relationships:
            if total_subjective_stress > 0 and char.relationships[source_id].trust > 0.5:
                # 信任度越高，背叛带来的伤害越大 (应力集中点 K_t)
                total_subjective_stress *= (1.0 + char.relationships[source_id].trust)
        
        char.sensation = total_tensile_stress - total_subjective_stress

        # --- Step 3: 受 (应变计算) ---
        # 物理计算：弹性应变，塑性扭曲增量，是否屈服
        elastic_strain, plastic_delta, is_yielded = MaterialPhysics.calculate_response(
            char.material, total_subjective_stress + total_tensile_stress # 正负向巨大的拉扯都会产生塑变
        )
        
        char.material.plastic_strain += plastic_delta

        # --- Step 4: 想 (相变判定与合金化) ---
        old_phase = char.material.phase
        new_phase = MaterialPhysics.check_phase_transformation(char.material)
        
        if new_phase and new_phase != old_phase:
            char.material.phase = new_phase
            # 发生相变，将永远改变角色的底层行为逻辑
            
        # --- Step 5 & 6: 行、识 (决策生成) ---
        # 默认决策逻辑 (数学保底)
        math_decision = self._math_decision(char, is_yielded)
        
        # 构造数学结果供决策参考
        math_context = {
            "sensation": char.sensation,
            "plastic_strain": char.material.plastic_strain,
            "is_yielded": is_yielded,
            "phase": char.material.phase.value
        }
        
        # 只有在重大事件、接近屈服点、或者发生塑性形变时，才调用 LLM 增强叙事，防止调用量爆炸
        should_call_llm = False
        allow_injection = False
        
        # 计算总的真实应力用于判断和展示
        total_stress_display = (total_subjective_stress + total_tensile_stress) * 100.0
        
        if self.use_llm and self.llm_engine:
            allow_injection = total_stress_display > (char.material.yield_point * 0.8)
            
            if allow_injection or is_yielded or stress.intensity > 0.3:
                should_call_llm = True
        
        if should_call_llm:
            prompt = self._build_prompt(char, event, stress, math_decision, total_subjective_stress, total_tensile_stress)
            llm_output = self.llm_engine.generate_action(prompt, allow_injection, math_context)
            
            if llm_output:
                final_decision = llm_output.decision_type
                narrative_log = f"[{final_decision.value}] {llm_output.action_description} (情感:{llm_output.emotion.value})"
                
                # 处理合金注入
                if llm_output.alloy_injection and allow_injection:
                    el = llm_output.alloy_injection.element
                    if el != "NONE":
                        alloy_log_msg = MaterialPhysics.inject_alloy(char.material, llm_output.alloy_injection)
                        alloy_log = f"\n    [灵魂炼金] 注入了 {llm_output.alloy_injection.concentration:.2f} 的 {el} 元素。原因: {llm_output.alloy_injection.reason} -> {alloy_log_msg}"
                        narrative_log += alloy_log
            else:
                # LLM 失败，回退到纯数学日志
                final_decision = math_decision
                narrative_log = f"[{final_decision.value}] 承受了 {total_stress_display:.1f} 的主观应力，基于相态({char.material.phase.value})做出了本能反应。"
                if is_yielded:
                    narrative_log += " [发生塑性形变]"
        else:
            # 纯数学计算分支
            final_decision = math_decision
            narrative_log = f"[{final_decision.value}] 承受了 {total_stress_display:.1f} 的主观应力，基于相态({char.material.phase.value})做出了本能反应。"
            if is_yielded:
                narrative_log += " [发生塑性形变]"

        # --- 记录记忆 (Episodic Memory) ---
        if total_subjective_stress > 0.1 or total_tensile_stress > 0.1:
            char.episodic_memories.append(EpisodicMemory(
                tick=tick_count,
                description=narrative_log,
                salience=plastic_delta + total_subjective_stress # 扭曲度越大的事记得越牢
            ))
            # 限制记忆池大小
            char.episodic_memories = sorted(char.episodic_memories, key=lambda x: x.salience, reverse=True)[:10]
            
            # 如果发生了塑性形变，触发深度反思 (Reflection)
            if plastic_delta > 0.3 and should_call_llm:
                self._trigger_reflection(char, "承受了极大的心理扭曲")

        # --- Step 7: 业 (状态写回) ---
        phase_event_log = None
        if new_phase and new_phase != old_phase:
            phase_event_log = f"{char.name} 的底层人格彻底改变了！从 {old_phase.value} 相变为了 {new_phase.value}！"
            
            # V11.0: 触发顿悟机制 (Reflection)
            if should_call_llm:
                self._trigger_reflection(char, "发生了彻底的材质相变")
                
        return self._generate_karma(char, final_decision, narrative_log, phase_event_log)

    def _math_decision(self, char: CharacterState, is_yielded: bool) -> DecisionType:
        """基于材质状态的纯数学决策映射"""
        mat = char.material
        
        # 1. 断裂态: 彻底崩溃
        if mat.phase == PhaseType.FRACTURE:
            return DecisionType.BREAKDOWN
            
        # 2. 马氏体 (黑化): 倾向于暴力屠杀
        if mat.phase == PhaseType.MARTENSITE:
            # 只要有一点不顺心(Sensation < 0)，就容易爆发
            if char.sensation < -0.2:
                return DecisionType.EXPLODE
            return DecisionType.ACT
            
        # 3. 奥氏体 (圣化): 倾向于牺牲和合作
        if mat.phase == PhaseType.AUSTENITE:
            return DecisionType.EXPLODE if char.sensation < -0.5 else DecisionType.ACT
            
        # 4. 渗碳体 (异化/暴发户): 极度自私，倾向于傲慢或掠夺
        if mat.phase == PhaseType.CEMENTITE:
            return DecisionType.EXPLODE if char.sensation > 0.5 else DecisionType.ACT
            
        # 5. 普通态 (珠光体)
        if is_yielded:
            # 压力过大，根据刚度/韧性比决定
            # 刚度高韧性低 -> 脆性反击 (EXPLODE)
            if mat.stiffness > mat.toughness * 1.5:
                return DecisionType.EXPLODE
            # 韧性高 -> 隐忍 (SUPPRESS)
            elif mat.toughness > mat.stiffness:
                return DecisionType.SUPPRESS
            else:
                return DecisionType.HESITATE
                
        return DecisionType.ACT
        
    def _build_prompt(self, char: CharacterState, event: OpenEvent, stress: PhysicalStress, math_decision: DecisionType, subjective_stress: float, tensile_stress: float) -> str:
        """构建 V10.0+ Prompt，包含最新记忆"""
        mat = char.material
        
        # 格式化合金成分
        elements_str = ", ".join([f"{k}:{v:.2f}" for k, v in mat.elements.items()]) if mat.elements else "无"
        
        # 格式化近期深刻记忆
        memories_str = "\n".join([f"- Tick {m.tick}: {m.description}" for m in char.episodic_memories[-3:]]) if char.episodic_memories else "- 无特别深刻的近期记忆"
        
        # 格式化关系与长期仇恨/恩情 (只提取与本次事件发起者相关的记忆)
        source_id = getattr(event, "source_entity_id", None)
        entity_memories_str = ""
        if source_id and source_id in char.relationships:
            rel = char.relationships[source_id]
            if rel.entity_memories:
                entity_memories_str = f"\n【你对引发此事的人的专属记忆】\n" + "\n".join([f"- {m}" for m in rel.entity_memories[-2:]])
                
        # 计算总的真实应力用于展示
        total_stress_display = (subjective_stress + tensile_stress) * 100.0
        
        return f"""
你叫 {char.name}，{char.age} 岁。{char.memory_summary}

【近期深刻记忆 (可能影响你现在的判断)】
{memories_str}{entity_memories_str}

【材质面板】
- 相态: {mat.phase.value} (决定了你的底层行为逻辑)
- 刚度(E): {mat.stiffness:.1f} (抵抗情绪波动)
- 韧性(T): {mat.toughness:.1f} (承受创伤总量)
- 屈服点: {mat.yield_point:.1f} / 你的主观真实承受应力: {total_stress_display:.1f}
- 塑性形变(扭曲度): {mat.plastic_strain:.2f}
- 体内合金: {elements_str}

【当前事件】
事件描述: {event.description}
维度冲击向量: {event.impact_vector}
物理应力类型: {stress.type.value} (客观物理强度: {stress.intensity*100:.1f})

【系统判定】
数学模型倾向于: {math_decision.value}

请生成你的反应。如果压力极大(超过屈服点)且你认为这会改变你的性格，请使用 alloy_injection 注入对应元素(C/S/Cr/Ni/P/Mn等)。
"""

    def _generate_karma(self, char: CharacterState, decision: DecisionType, log: str, phase_event: Optional[str]) -> KarmaWriteback:
        """生成业力，根据材质状态放大影响，并根据决策指定具体资源的损耗"""
        wb = KarmaWriteback(entity_id=char.id, decision=decision, narrative_log=log, triggered_phase_event=phase_event)
        
        # 相态修饰
        is_martensite = char.material.phase == PhaseType.MARTENSITE
        is_austenite = char.material.phase == PhaseType.AUSTENITE
        is_cementite = char.material.phase == PhaseType.CEMENTITE
        
        if decision == DecisionType.EXPLODE:
            if is_martensite:
                wb.conflict_delta = 1.5
                wb.resource_deltas[ResourceDim.SOMATIC] = -0.5 
                wb.resource_deltas[ResourceDim.MATERIAL] = -0.5
            elif is_austenite:
                wb.cooperation_delta = 1.5
                wb.resource_deltas[ResourceDim.SOMATIC] = 0.2
                wb.resource_deltas[ResourceDim.IDEOLOGICAL] = 0.8
            elif is_cementite:
                wb.conflict_delta = 1.0
                wb.resource_deltas[ResourceDim.SOCIAL] = -0.5
                wb.resource_deltas[ResourceDim.MATERIAL] = 0.5
            else:
                wb.conflict_delta = 0.5
                wb.resource_deltas[ResourceDim.SOMATIC] = -0.2
        elif decision == DecisionType.ACT:
            if is_austenite:
                wb.cooperation_delta = 0.2
            else:
                wb.conflict_delta = 0.1
        elif decision == DecisionType.SUPPRESS:
            # 隐忍可能意味着为了保住权力而花钱行贿
            if char.desire_matrix.get(ResourceDim.SOCIAL, 0.0) > 0.8:
                wb.resource_deltas[ResourceDim.MATERIAL] = -0.2
                wb.resource_deltas[ResourceDim.SOCIAL] = 0.1 # 花钱买平安
        elif decision == DecisionType.BREAKDOWN:
            wb.conflict_delta = 0.2 # 被动引发混乱
            
        return wb
        
    def _trigger_reflection(self, char: CharacterState, trigger_reason: str):
        """V11.0 反思机制: 总结长期记忆，修改 Desires"""
        if not self.use_llm or not self.llm_engine: return
        
        # TODO: 将 Episodic Memories 交给 LLM 总结成 memory_summary
        # 并基于创伤经历微调 desire_matrix (Desire Conservation)
        pass