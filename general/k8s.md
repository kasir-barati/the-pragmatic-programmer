# Kubernetes

## Minikube

1. [Install `kubectl` command line tool](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux).
2. Make sure virtualization is enabled: `grep -E --color 'vmx|svm' /proc/cpuinfo`.
   <img width="2036" height="754" alt="image" src="https://github.com/user-attachments/assets/de003463-8052-4727-b3d3-ab40aac8f00d" />
3. You can also run Minikube without a Hyporvisor, but having one make sure you are not messing your linux setup.
   1. Download it for your Linux distro: https://www.virtualbox.org/wiki/Linux_Downloads.
   2. Then install it.
3. https://minikube.sigs.k8s.io/docs/start.

### Check Minikube Works

1. Open the Oracle VirtualBox and make sure you have virual machine for Minikube:
   <img width="1920" height="814" alt="image" src="https://github.com/user-attachments/assets/cedc74dd-4383-419e-9f70-a838d3f1476b" />
2. `minikube status` should return:
   ```
   minikube
   type: Control Plane
   host: Running
   kubelet: Running
   apiserver: Running
   kubeconfig: Configured
   ```
3. `kubectl get nodes` should return:
   ```
   NAME       STATUS   ROLES           AGE   VERSION
   minikube   Ready    control-plane   19m   v1.35.1
   ```
4. `kubectl create deployment hello-minikube --image=kicbase/echo-server:1.0`.
5. `kubectl expose deployment hello-minikube --type=NodePort --port=8080`.
6. `kubectl get deployments.apps`.
7. `minikube service hello-minikube --url`.
8. Open it in your browser and you should see the service's details. It is essentially somewhat similar to the defaul Nginx home page when you install Nginx.
9. Now do NOT forget to clean up:
   1. `kubectl delete services hello-minikube`.
   2. `kubectl delete deployment hello-minikube`.
10. And now you should NOT see any pods: `kubectl get pods`.
