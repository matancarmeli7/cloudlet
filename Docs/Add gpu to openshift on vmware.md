# Add gpu to openshift on vmware

## Steps to reproduce: 
1. Enable gpu on host
2. Enable gpu on vm
3. Deploying gpu on openshift

## Enable gpu on host

## Enable gpu on vm
1. Make sure your vm boot mode is UEFI\EFI
2. Add pci device on vm settings (you showld see your gpu device)
3. go to Edit Settings -> VM Options ->Advanced -> Configuration Parameters -> Edit Configuration.
 Add these 3 parameters:
  * pciPassthru.use64bitMMIO=TRUE
  * pciPassthru.64bitMMIOSizeGB=64
  * hypervisor.cpuid.v0=FALSE
4. Power on the vm.

## Deploying gpu on openshift
For deploying gpu operator you can follow redhat guide https://access.redhat.com/solutions/4908611 and use the gpu operator git https://github.com/NVIDIA/gpu-operator .
If you'r in disconnected environment use this git https://github.com/dmc5179/nvidia-driver and build the driver image by yourself with the kernel version you need.
After that you can use the opertaor and just change the image that the daemonset uses for deploying the driver.

 
