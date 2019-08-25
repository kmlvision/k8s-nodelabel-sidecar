import os
import logging

from k8s_labelreader import K8SLabelReader

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s: %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)


def configure():
    kubectl_config = os.environ.get('KUBECTL_CONFIG')
    node_name = os.environ.get('NODE_NAME')
    node_labels = os.environ.get('NODE_LABELS', '').split(',')
    env_names = os.environ.get('ENV_NAMES', '').split(',')

    labelReader = K8SLabelReader(kubectl_config=kubectl_config, node_name=node_name, node_labels=node_labels,
                                 env_names=env_names)
    return labelReader


def main():
    label_reader = configure()
    node_label_envs = label_reader.read_labels()

    target_env_file = os.environ.get('ENV_FILE', 'k8s_nodelabel_envs')
    with open(target_env_file, 'w') as fout:
        for label_env in node_label_envs.items():
            fout.write('%s=%s\n' % (label_env[0], label_env[1]))


if __name__ == "__main__":
    main()
