from typing import Tuple, Optional
from .types import MaterialState, PhaseType, AlloyInjection

class MaterialPhysics:
    """人格材料力学引擎 (V10.0)"""

    @staticmethod
    def calculate_response(material: MaterialState, subjective_stress_intensity: float) -> Tuple[float, float, bool]:
        """
        计算材料的应力响应
        Returns: (elastic_strain, plastic_delta, is_yielded)
        """
        elements = material.elements
        ep = material.plastic_strain
        
        # 1. 脆性断裂判定
        # 如果承受的压力超过断裂点、或者塑性形变过大，或者硫含量过高
        if ep > 1.0 or elements.get("S", 0.0) > 0.2:
            return 0.0, 0.0, True # 已经断裂，不再计算理性应力
            
        # 2. 动态参数修正 (合金强化/退火效应)
        effective_E = material.stiffness
        effective_T = material.toughness
        
        # 碳(C) 固溶强化：提高刚度，降低韧性
        if "C" in elements:
            effective_E += elements["C"] * 5.0
            effective_T -= elements["C"] * 2.0
            
        # 镍(Ni) 韧化：降低刚度，提高韧性
        if "Ni" in elements:
            effective_E -= elements["Ni"] * 3.0
            effective_T += elements["Ni"] * 8.0
            
        effective_E = max(0.1, effective_E)
        effective_T = max(0.1, effective_T)

        # 3. 屈服判定
        applied_stress = subjective_stress_intensity * 100.0
        
        # 漏洞四修复：断裂点 (break_point) 真正生效
        if applied_stress >= material.break_point:
            # 直接导致极大的塑性形变，确保下一阶段必定触发断裂相变
            is_yielded = True
            elastic_strain = material.yield_point / effective_E
            plastic_delta = 2.0 # 强制超过 1.0 的断裂阈值
            return elastic_strain, plastic_delta, is_yielded
            
        if applied_stress < material.yield_point:
            # 弹性阶段：情绪波动
            elastic_strain = applied_stress / effective_E
            plastic_delta = 0.0
            is_yielded = False
        else:
            # 塑性阶段：人格扭曲
            elastic_strain = material.yield_point / effective_E
            excess_stress = applied_stress - material.yield_point
            # 加工硬化系数，韧性越低硬化越快
            hardening_factor = 1.0 / effective_T
            plastic_delta = excess_stress * hardening_factor * 0.01
            is_yielded = True
            
        return elastic_strain, plastic_delta, is_yielded

    @staticmethod
    def check_phase_transformation(material: MaterialState) -> Optional[PhaseType]:
        """判定是否发生相变"""
        ep = material.plastic_strain
        elements = material.elements
        
        if ep > 1.0 or elements.get("S", 0.0) > 0.2:
            return PhaseType.FRACTURE
            
        if ep > 0.5:
            c_content = elements.get("C", 0.0)
            ni_content = elements.get("Ni", 0.0)
            
            if c_content > 0.1:
                return PhaseType.MARTENSITE # 高碳高扭曲 -> 黑化
            elif ni_content > 0.1:
                return PhaseType.AUSTENITE # 高镍高扭曲 -> 圣徒化
            else:
                return PhaseType.CEMENTITE # 暴发户/异化态
                
        return None

    @staticmethod
    def inject_alloy(material: MaterialState, injection: AlloyInjection) -> str:
        """注入合金元素，改变材料底色"""
        el = injection.element
        conc = injection.concentration
        material.elements[el] = material.elements.get(el, 0.0) + conc
        
        log = ""
        if el == "C":
            material.stiffness += conc * 10.0
            material.toughness = max(0.1, material.toughness - conc * 5.0)
            material.yield_point += conc * 2.0
            log = f"心智硬化，刚度升至 {material.stiffness:.1f}，韧性降至 {material.toughness:.1f}"
        elif el == "S":
            material.break_point = max(0.1, material.break_point - conc * 10.0)
            log = f"心智腐蚀，崩溃阈值剧降至 {material.break_point:.1f}"
        elif el == "Ni":
            material.toughness += conc * 15.0
            material.stiffness = max(0.1, material.stiffness - conc * 2.0)
            log = f"心智柔化，韧性飙升至 {material.toughness:.1f}"
        elif el == "Cr":
            material.yield_point += conc * 5.0
            log = f"心智防腐，屈服点升至 {material.yield_point:.1f}"
        elif el == "P":
            material.yield_point = max(0.1, material.yield_point - conc * 5.0)
            material.break_point = max(0.1, material.break_point - conc * 5.0)
            log = f"防线全面溃败，屈服点和崩溃阈值双双下降"
        elif el == "Mn":
            material.stiffness += conc * 5.0
            material.toughness += conc * 5.0
            log = f"变得坚忍耐磨，刚度和韧性双双上升"
            
        return log