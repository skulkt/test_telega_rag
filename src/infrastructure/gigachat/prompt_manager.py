import yaml
import os


class PromptManager:
    prompts_file_name = "prompt.yaml"

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file_path = os.path.join(
            current_dir, "../../", self.prompts_file_name
        )

        self.prompts = self._load_prompts()

    def _load_prompts(self):
        try:
            with open(self.config_file_path) as prompts_file:
                return yaml.safe_load(prompts_file)
        except FileNotFoundError:
            raise ValueError("Файл с описаниями промтов не найден")

    def get_prompt(self, agent_name: str):
        agent_cfg = self.prompts.get("agents", {}).get(agent_name)

        if not agent_cfg:
            raise ValueError(f"Агент '{agent_name}' не найден в конфигурации")

        prompt = agent_cfg.get("system", "")

        return prompt
