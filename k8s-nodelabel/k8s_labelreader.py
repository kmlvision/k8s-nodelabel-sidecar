#!/usr/bin/env python3
import os
import logging

from kubernetes import client, config

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s: %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)


class K8SLabelReader(object):

    def __init__(self, kubectl_config, node_name, node_labels, env_names):
        """
        Create a new K8S Label Reader
        :param kubectl_config: the location of the kubectl config file
        :param node_name: the name of the node whose labels need to be read
        :param node_labels: the desired node labels to read
        :param env_names: the desired env names (needs to be of the same size as node_labels)
        """

        self.kubectl_config = kubectl_config
        assert self.kubectl_config not in (None, '') and os.path.exists(os.path.abspath(self.kubectl_config)), \
            "kubernetes config file does not exist in '{}'".format(self.kubectl_config)

        self.node_name = node_name
        assert self.node_name not in (None, ''), "node_name must not be null or empty"

        self.node_labels = node_labels
        assert self.node_labels is not None and len(
            self.node_labels) > 0, "node_labels must be specified by least 1 label"

        self.env_names = env_names
        assert self.env_names is not None and len(self.env_names) == len(
            self.node_labels), "env_labels must be specified and be of same size as node_labels"

    def read_labels(self):
        # Configs can be set in Configuration class directly or using helper utility
        config.load_kube_config(config_file=self.kubectl_config)

        v1 = client.CoreV1Api()
        log.info("listing node labels for node: {}".format(self.node_name))
        node = self.find_node(v1.list_node(), self.node_name)
        assert node is not None, "specified node not found"

        node_label_envs = {}
        for i, label in enumerate(self.node_labels):
            key = label
            value = node.metadata.labels.get(key);
            env_name = self.env_names[i]
            node_label_envs[env_name] = value

        return node_label_envs

    @staticmethod
    def find_node(node_list, node_name):
        for i in node_list.items:
            if i.metadata.name == node_name:
                return i
        return None
