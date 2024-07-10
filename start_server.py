import yaml
import argparse
from uvicorn.main import run

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('--port', default=8000, type=int)
    args = argp.parse_args()
    with open('logger.yaml') as fd:
        log_config = yaml.safe_load(fd)
    run('main:app', host='0.0.0.0', port=args.port, reload=True, use_colors=True, log_config=log_config)
