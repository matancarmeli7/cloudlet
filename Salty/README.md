#### Salty v 0.1.0
This version of Salty is a prototype. For now it scans a local registry and compares the images digests with the same images of a remote registry.

# Salty v 0.1.1
New in this version:
* Logging to splunk the unmatched images.
* Running scan every 30 min
* Getting local quay in a generic way

### Future Versions
* Develop as a GO OCP Operator to have control over OpenShift use of Images.
* Add cache for disconnected checks.
* Alert Cloud Splunk of problems.
* Get authentication token from secret, don't have it in the code as clear text.
* Don't scan local images that aren't in mirror state.
