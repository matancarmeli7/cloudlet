# Argocdod-tests
* A centralized repository that contains tests for deployed applications.
* All tests are written in **Ansible** as seperate tasks beside the main playbook in the ```tasks/``` folder.
* This repository complements the [argocdod](https://github.com/matancarmeli7/cloudlet/tree/master/argocdod) repository.

## Writing new tests
* Write a task that defines your test (Checks that a ```Pod``` is ready/That a ```Route``` responds/etc.).
* If your test needs additional files put them in the ```yamls/``` folder.
* Make sure your test conforms to the following requirements:
  * Write your whole task in a block.
  * Add this **rescue** clause to your block.
  ```
  rescue:
     - name: Setting test error message
       set_fact:
         err_ms: "TASK: {{ ansible_failed_task.name }} FAILED WITH MSG: {{ ansible_failed_result.msg }}"
         
     - name: Updating failed_tests
       set_fact:
         failed_tests: "{{ failed_tests + [ err_ms ] }}"
  ```
  * Make sure your test cleans up after itself using an **always** clause, e.g this cleans whatever resources that were created with the file minio-instance.yml:
  ```
    always:
      - name: Undeploy YAML
        k8s:
          definition: "{{ lookup('file', 'yamls/minio-instance.yml') }}"
          state: absent
          namespace: argocdod
          kubeconfig: "{{ kubeconfig_path }}"
  ```
