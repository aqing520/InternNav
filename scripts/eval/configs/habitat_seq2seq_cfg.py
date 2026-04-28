from internnav.configs.agent import AgentCfg
from internnav.configs.evaluator import EnvCfg, EvalCfg, TaskCfg
from internnav.configs.model import seq2seq_eval_cfg

eval_cfg = EvalCfg(
    agent=AgentCfg(
        server_port=8087,
        model_name='seq2seq',
        ckpt_path='checkpoints/r2r/fine_tuned/seq2seq',
        model_settings=seq2seq_eval_cfg.dict(),
    ),
    env=EnvCfg(
        env_type='habitat',
        env_settings={
            'config_path': 'scripts/eval/configs/vln_r2r.yaml',
            'episode_limit': 1,
        },
    ),
    task=TaskCfg(
        task_name='habitat_seq2seq_eval',
    ),
    eval_type='habitat_evaluator',
    eval_settings={
        'output_path': './logs/habitat/seq2seq_smoke',
        'save_video': False,
        'epoch': 0,
        'max_steps_per_episode': 500,
        'use_agent_server': True,
        'port': '2333',
        'dist_url': 'env://',
    },
)
