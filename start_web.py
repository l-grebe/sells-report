import yaml
import setting

from uvicorn.main import run
from logging import config as logging_config

if __name__ == "__main__":
    with open("logger.yaml", encoding="utf-8") as fd:
        log_config = yaml.safe_load(fd)
    run(
        "main:app",
        host=setting.default_setting.host,
        port=setting.default_setting.port,
        reload=setting.default_setting.debug,
        log_config=log_config,
    )