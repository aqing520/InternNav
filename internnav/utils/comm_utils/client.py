import base64
import pickle
from typing import Any, Dict, List, Optional

import requests

from internnav.configs.agent import AgentCfg, InitRequest, ResetRequest, StepRequest


def serialize_obs(obs):
    serialized = pickle.dumps(obs)
    encoded = base64.b64encode(serialized).decode('utf-8')
    return encoded


def _dump_model(model):
    if hasattr(model, 'model_dump'):
        return model.model_dump(mode='json')
    return model.dict()


class AgentClient:
    """
    Client class for Agent service.
    """

    def __init__(self, config: AgentCfg):
        self.base_url = f'http://{config.server_host}:{config.server_port}'
        self.agent_name = self._initialize_agent(config)

    def _initialize_agent(self, config: AgentCfg) -> str:
        request_data = _dump_model(InitRequest(agent_config=config))

        response = requests.post(
            url=f'{self.base_url}/agent/init',
            json=request_data,
            headers={'Content-Type': 'application/json'},
        )
        response.raise_for_status()

        return response.json()['agent_name']

    def step(self, obs: List[Dict[str, Any]]) -> List[List[int]]:
        request_data = _dump_model(StepRequest(observation=serialize_obs(obs)))

        response = requests.post(
            url=f'{self.base_url}/agent/{self.agent_name}/step',
            json=request_data,
            headers={'Content-Type': 'application/json'},
        )
        response.raise_for_status()

        return response.json()['action']

    def reset(self, reset_index: Optional[List] = None) -> None:
        response = requests.post(
            url=f'{self.base_url}/agent/{self.agent_name}/reset',
            json=_dump_model(ResetRequest(reset_index=reset_index)),
            headers={'Content-Type': 'application/json'},
        )
        response.raise_for_status()
