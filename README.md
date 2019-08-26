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

## HTTP respopnse 403 Forbidden when accessing node info
depending on the envrionment in which k8s-nodelabel-sidecar is running, you may encounter the following response
```json
 {
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "nodes is forbidden: User \"system:serviceaccount:myNamespace:default\" cannot list resource \"nodes\" in API group \"\" at the cluster scope",
  "reason": "Forbidden",
  "details": {
    "kind": "nodes"
  },
  "code": 403
}
``` 

Most probably this occurs when you use the in-cluster config and the default service-account does not have sufficient privileges to access the `nodes` and `nodes/status` resources.
In that case you could add a `ClusterRole` and `ClusterRoleBinding` to your cluster to add those privileges for the affected service account:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  # "namespace" omitted since ClusterRoles are not namespaced
  name: node-info
rules:
  - apiGroups: [""]
    resources: ["nodes", "nodes/status"]
    verbs: ["get", "list"]
---
# bind the default service-account to the node-info clusterrole
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-node-info-default
subjects:
  - kind: ServiceAccount
    name: default
    namespace: myNamespace
roleRef:
  kind: ClusterRole
  name: node-info
  apiGroup: rbac.authorization.k8s.io
```
