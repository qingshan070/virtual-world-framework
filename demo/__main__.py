import argparse
import os
from .engine import SimulationEngine
from .types import InteractionMode

def main():
    parser = argparse.ArgumentParser(description="VWI Demo: 虚拟世界基础设施闭环演示 (包含LLM双向绑定)")
    parser.add_argument("--ticks", type=int, default=10, help="运行的 Tick 数量")
    parser.add_argument("--use-llm", action="store_true", help="是否开启 LLM 增强叙事与微调")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="LiteLLM 模型名称")
    parser.add_argument("--interactive", action="store_true", help="是否开启交互模式，逐 Tick 暂停")
    
    # Issue 10.2: 在 CLI 暴露核心能力
    parser.add_argument("--mode", type=str, choices=["GOD", "ARCHON", "AVATAR"], default="GOD", help="交互模式: GOD(自然语言沙盒), ARCHON(政策指令), AVATAR(角色扮演)")
    parser.add_argument("--avatar", type=str, default="char_0", help="AVATAR 模式下扮演的角色ID (默认为 char_0)")
    parser.add_argument("--population", type=int, default=4, help="初始生成的人口数量")
    parser.add_argument("--seed", type=int, default=42, help="随机数种子，保证可复现性")
    
    args = parser.parse_args()
    
    if args.use_llm and not os.environ.get("OPENAI_API_KEY"):
        print("警告: 开启了 --use-llm 但未检测到 OPENAI_API_KEY 环境变量。")
        print("LiteLLM 需要对应的 API Key。如果是本地模型请配置相应的环境变量。")
        print("将尝试继续运行，如果失败会自动 Fallback 到数学模板。\n")
        
    mode_enum = InteractionMode(args.mode)
        
    engine = SimulationEngine(
        use_llm=args.use_llm, 
        model_name=args.model,
        mode=mode_enum,
        avatar_id=args.avatar,
        population=args.population,
        seed=args.seed
    )
    engine.run(ticks=args.ticks, interactive=args.interactive)
    
    print("\n=== 模拟结束 ===")
    print(f"完整日志已保存至 {engine.log_file}")

if __name__ == "__main__":
    main()