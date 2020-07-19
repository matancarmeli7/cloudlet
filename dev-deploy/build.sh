#!/bin/bash
# Use vfs with buildah. Docker offers overlayfs as a default, but buildah
# cannot stack overlayfs on top of another overlayfs filesystem.
export STORAGE_DRIVER=vfs

# Newer versions of podman/buildah try to set overlayfs mount options when
# using the vfs driver, and this causes errors.
sed -i '/^mountopt =.*/d' /etc/containers/storage.conf


for dir in $(ls -d apps/*/) ; do
  cd $dir
  if [ -d "build" ]; then
    echo " "
    cd build
    PARENT_DIR=$(basename "${PWD%/*}")
    IMAGE_NAME="cloudlet/$PARENT_DIR"

    TAG="${1}"
    REGISTRY="${2}"

    buildah bud -t ${REGISTRY}/${IMAGE_NAME}:${TAG} -t ${REGISTRY}/${IMAGE_NAME}:latest .
    echo " "
    echo "Build complete, pushing to registry"
    buildah push --tls-verify=false ${REGISTRY}/${IMAGE_NAME}:${TAG} docker://${REGISTRY}/${IMAGE_NAME}:${TAG}
    buildah push --tls-verify=false ${REGISTRY}/${IMAGE_NAME}:latest docker://${REGISTRY}/${IMAGE_NAME}:latest
    cd ..
    echo " "
  else
    echo "!!! build folder not found in ${dir} !!!"
  fi

  cd ../..
done
