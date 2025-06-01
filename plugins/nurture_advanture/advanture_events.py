import yaml
import os
import random

# 加载所有可用事件
events_path = "./data/nurture_advanture/events"
events_files = os.listdir(events_path)
events = []

for event_file in events_files:
    filename = os.path.join(events_path, event_file)
    with open(filename, "r", encoding="utf-8") as f:
        event = yaml.load(f, yaml.FullLoader)
        events.append(event)

class AdvantureResult():
    name: str = ""
    text: str = ""
    rewards: dict = {}

def get_advanture(usr_skills: list[str]) -> AdvantureResult:
    """抽取一个探险事件"""
    # 先随机选择一个事件
    event = None
    while True:
        event = random.choice(events)
        # 权重随机
        if random.randint(1, 100) <= event["weight"]:
            break
    
    # 根据技能确定奖励
    for result_info in event["results"]:
        result = AdvantureResult()
        if (not result_info["skill"]) or (result_info["skill"] in usr_skills):
            result.name = event["name"]
            result.text = result_info["text"]
            result.rewards = result_info["rewards"]
    
    return result

if __name__ == "__main__":
    result = get_advanture(["打窝"])
    print(result.name, result.text, result.rewards)