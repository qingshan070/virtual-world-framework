from typing import List, Dict, Any
import random
from .types import ResourceDim, OpenEvent, StressType

class VesselEngine:
    """器世间引擎 (V10.0): 负责外部物理环境的自然演化与事件扩散"""
    def __init__(self, region_id: str):
        self.region_id = region_id
        
        # 环境资源存量
        self.resources: Dict[ResourceDim, float] = {
            ResourceDim.SOMATIC: 100.0,
            ResourceDim.MATERIAL: 100.0,
            ResourceDim.SOCIAL: 100.0,
            ResourceDim.IDEOLOGICAL: 100.0
        }
        
        # 宏观环境状态
        self.conflict_level = 0.0     # 冲突度
        self.cooperation_level = 0.0  # 合作度
        self.entropy = 0.0            # 环境熵(污染度)
        
    def process_tick(self, character_writebacks: List[Any]) -> List[OpenEvent]:
        """演化一个 Tick，吸收角色的业力写回，产出环境自然事件"""
        
        # 1. 吸收角色写回 (Karma Resolution)
        for wb in character_writebacks:
            for dim, delta in wb.resource_deltas.items():
                self.resources[dim] += delta
            
            self.conflict_level += wb.conflict_delta
            self.cooperation_level += wb.cooperation_delta
            
        # 2. 环境自然代谢
        self.conflict_level *= 0.95
        self.cooperation_level *= 0.95
        
        # 资源透支惩罚
        for dim, val in self.resources.items():
            if val < 0:
                self.conflict_level += 0.1
                self.resources[dim] = 0.0 # 强制归零，但不消除冲突后果
                
        # 3. 产出环境自然事件 (自发涌现)
        events = []
        
        # 修复7：世界层的正反馈闭环 (合作带来的建设与复苏)
        if self.cooperation_level > 1.0:
            events.append(OpenEvent(
                id=f"evt_coop_{random.randint(1000,9999)}",
                description=f"人们齐心协力(合作值:{self.cooperation_level:.1f})，共同开展灾后重建与互助。",
                impact_vector={ResourceDim.SOMATIC: 0.4, ResourceDim.MATERIAL: 0.3, ResourceDim.SOCIAL: 0.2, ResourceDim.IDEOLOGICAL: 0.5},
                stress_type=StressType.TENSILE
            ))
            
        # 饥荒/瘟疫判定 (肉体生存危机)
        if self.resources[ResourceDim.SOMATIC] < 20.0 and random.random() < 0.2:
            events.append(OpenEvent(
                id=f"evt_famine_{random.randint(1000,9999)}",
                description="本区域爆发了严重的饥荒，生存物资极度匮乏。",
                impact_vector={ResourceDim.SOMATIC: -0.8, ResourceDim.MATERIAL: -0.5},
                stress_type=StressType.COMPRESSIVE
            ))
            
        # 战乱判定 (高冲突度)
        if self.conflict_level > 2.0 and random.random() < 0.3:
            events.append(OpenEvent(
                id=f"evt_war_{random.randint(1000,9999)}",
                description="冲突不可调和，爆发了大规模的流血骚乱！",
                impact_vector={ResourceDim.SOMATIC: -0.5, ResourceDim.MATERIAL: -0.8, ResourceDim.SOCIAL: -0.5},
                stress_type=StressType.SHEAR
            ))
            
        return events