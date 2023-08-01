<h1>How to run locally</h1>

- Create a venv:

``` bash
python3 -m venv .     
```
- Activate it:

``` bash
source ./bin/activate
```
- Install the requirement:

``` bash 
pip3 install --no-cache-dir -r requirements.txt 
```

- Run it:

``` bash 
python3 main.py  
```

- be happy :)


<h1>How to run in kubernetes using minikube</h1>

Prerequisites:

- <a href="https://kubernetes.io/docs/tasks/tools/">kubectl</a>
- <a href="https://minikube.sigs.k8s.io/docs/start/">minikube</a>
- <a href="https://helm.sh/docs/intro/install/">helm</a>
- <a href="https://k8slens.dev/">lens</a>

<hr/>


Start your local cluster:

``` bash
minikube start
```

Go to the <b>/project/kubernetes/charts</b> folder and run the following commands to install the <b>metrics-server</b> and the <b>postgresql database</b> in your k8s cluster:

``` bash
helm install metrics-server metrics-server/metrics-server -f metrics-values.yaml --namespace=kube-system
```

``` bash
helm install my-postgresql bitnami/postgresql -f values-postgresql.yaml --namespace=postgresql --create-namespace 
```

Run the following commands to deploy the ArgoCD

``` bash
kubectl create namespace argocd
```

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Create the namespace for your application in your cluster:

``` bash
kubectl create namespace my-app
```

Go to the folder <b>/kubernetes</b> and apply the  secrets in yout cluster:

```bash
kubectl apply -k secrets/
```
After applying the secrets you will be able to deploy your application using the <b>ArgoCD</b>

To access the application we need to port forward the service, first get the pod's name:
``` bash
kubectl get pods -n my-app
```

Replace the pod's name in the command below:

``` bash
kubectl port-forward pods/<pods name> 5000:5000 -n my-app
```

Access the application in the browser at: <b>localhost:5000</b>

- be happy :)

