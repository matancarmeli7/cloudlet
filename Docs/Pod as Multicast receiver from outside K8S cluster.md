# Pod as Multicast receiver from outside K8S cluster
 
In order to enable Pod to receive multicast from outside the k8s cluster there are few prerequisites that need to be accomplished. 
First, let’s understand why it can't work by default.
Kubernetes has its own network so pods can talk with each other in the same project and also reach the outside world.
Each pod has an interface named eth0 and an internal ip. All routes related to this interface are immutable – which means that even if there is an additional interface attached to the pod (multus allows us to do that), it can’t use the routes that are related to the default interface(eth0).
This is a view from inside a pod, you can see the routes related to eth0 - they will remain as is, they cannot be changed.

**Short brief of multicast:**

Every network has multicast range addresses (224.0.0.0/4), a source/sender for the multicast and a receiver.
For the receiver side to work it has to join the multicast group address that the sender is sending message to and make sure that both multicast address and the source address are routable.
In our case it looks like that:

**The solution:**

To use multicast group address you need to join multicast group, and since the only interface that is available is the default one, every request will be assigned to the pod default network interface and will be requested from the internal network multicast group range, so the request doesn’t reach outside the cluster.
To solve this issue, you can add another network interface with one of Multus CNI plug-in to the pod, and mention explicitly the addresses of the multicast group and the multicast source in the routes section.
In order to do that you can use red hat documentation.
After choosing your plugin according to you network architecture make sure your routes are ok.
In case you are unaware of the source address you can make a multicast request from a host and not from kubernetes cluster and run tcpdump. You will see the source ip sending packets to the multicast group address.
 In our case we used ipvlan and the routes were like this:
 
"routes": [ { "dst": "<multicast group ip address>"},{"dst": "<multicast source ip address>"}
After configuring the new network you need to attach it to a pod , just add an annotation to your pod:
k8s.v1.cni.cncf.io/networks: <network>
That’s it now you can receive multicast to your pod from outside kubernetes cluster.
