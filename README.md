# k8s-nodelabel-sidecar

A simple docker image that uses the kubernetes-python client to access the kubernetes api of a specified cluster and write the specified labels to an .env file. You may use the image as an init-container for a pod that writes the .env file to a shared volume. You could then `source` the label values written in the .env file from any other container of the pod.

## configuration
To configure the k8s-nodelabel-sidecar image, you can set the following env-variables

* `NODE_NAME`: the name of the node of which the labels should be read (will most often be set to a downWardApi `spec.nodeName` in the container config, to refer to the actual node where the pod is scheduled)
* `NODE_LABELS`: a comma-separated list of labels that should be read from the node specified with `NODE_NAME`
* `ENV_NAMES`: a comma-separated list of env-variable names that are used to store the values of the labels specified with `NODE_LABELS` (must be the same number as node labels are specified)
* `ENV_FILE`: the file to write the env variables as `EXPORT NAME=VALUE` to be later used with `source`
* `KUBECTL_CONFIG`: optional, points to a valid kubectl config file to access the cluster (only needed if you use this from outside a k8s-cluster). If not set, the default in-cluster config will be used (should be sufficient if you intend to run this image from within a k8s-cluster)

```.env
KUBECTL_CONFIG=/kubeconfig
NODE_NAME=myNode
NODE_LABELS=kubernetes.io/hostname,kubernetes.io/os
ENV_NAMES=HOSTNAME,HOST_OS
ENV_FILE=/node-labels.env
```
