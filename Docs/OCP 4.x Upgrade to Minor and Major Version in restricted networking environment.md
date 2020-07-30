#
**_OCP 4.x Upgrade to Minor and Major Version in Disconnected environment_**

Main goals of updates/upgrades - bug fixes, new features, security vulnaribilities fixes, where ideal state is always be up to date.
Updates/upgrades can be done to the latest minor version of the existing current major version or to the next major version. 
For instance, if you deployed your cluster when the latest version was 4.3.22 you can upgrade it today to the latest minor 4.3.29 version 
or gradually to the latest existing version,i.e ocp 4.5.4.
In restricted networks this process includes additional steps of mirroring the relevant images in your existing private registry and changing 
configuration of several cluster components that will allow you to perform upgrade smoothly.

