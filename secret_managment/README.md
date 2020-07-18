# Secrets management using HashiCorp Vault & GoDaddy External Secrets

## Architecture & Implementation
![Architecture](https://i.imgur.com/Ovk4GPn.jpg)

In the main cloud, a HashiCorp Vault HA cluster will be installed that will hold all of our clients' secrets.
Using the External Secrets Kubernetes Operator by GoDaddy, each cloudlet can fetch data from Vault and create regular Kubernetes secrets from it. It does that using an ExternalSecret CRD, which defines how to create a Kubernetes secret from Vault data, assigning values from keys in a secret engine to Kubernetes Secret properties.

### Workflow steps
1. Operator requests information about all the `ExternalSecrets` resources in its namespace from the API server.
2. API server responds with `ExternalSecrets` resources.
3. Operator fetches secrets data using the `ExternalSecret` definition from Vault.
4. Vault responds with secrets data if the operator authenticated successfully and is permitted to read them.
5. The operator upserts `Secrets` with the fetched data.
6. Pods can access `Secrets` normally.

### Example
With the following ExternalSecret example, the operator will create a Secret named `oris-secret`, mapping the value of a key named `dod` from a **secret** named `dodori` in an enabled K/V 2 **secret engine** named `kv2secrets`, assigning its value to a property named `ori` in a Kubernetes Secret. To create the secret, the operator authenticates to an enabled kubernetes **authentication method** at the path `preprod`. For this to work, a **role** named  `external-secrets-role` needs to be defined at the **authentication method**, granting the operator's Service Account readonly permissions to the **secret engine** secrets. It does that by mapping a predefined **policy** to the generated **tokens** of the **role**.
*This example uses one value from a key, but an ExternalSecret can contain multiple keys/values if needed. To do that add values to spec.data as you wish*
```
apiVersion: 'kubernetes-client.io/v1'
kind: ExternalSecret
metadata:
  name: oris-secret
spec:
  backendType: vault
  vaultMountPoint: preprod
  vaultRole: external-secrets-role
  data:
  - key: kv2secrets/data/dodori
    name: dod
    property: ori
```
The operator creates this Secret from the ExternalSecret:
```
apiVersion: v1
kind: Secret
data:
  ori: **** (dod's value base64 encoded)
type: Opaque
```
If all of the values from a Vault secret are needed, a less repetitive ExternalSecret syntax can be used:
```
apiVersion: 'kubernetes-client.io/v1'
kind: ExternalSecret
metadata:
  name: oris-full-secret
spec:
  backendType: vault
  vaultMountPoint: preprod
  vaultRole: external-secrets-demo-role
  dataFrom:
  - kv2secrets/data/dodori
```
---
## Vault terms

### Secret Engines

* A secret engine is where Vault secrets are created and maintained. Each secret engine kind defines the format/source of secrets and are different by their purposes.
* Each project will have its own K/V 2 secret engine with full permissions to it, named after the project's name. 
* K/V 2 stands for Key/Value Version 2. It's a secret engine where the secrets are stored and accessed in a key-value manner. Version 2 supplies us versioning - each secret can maintain versions, allowing to roll back or forward between versions (configurations).
* https://learn.hashicorp.com/vault?track=secrets-management#secrets-management
---
### Authentication methods
* In order to login/authenticate to Vault an authentication method should be previously enabled.
* Authentication methods set "authentication endpoints", allowing to authenticate from different providers (local and remote).
* For example, the `userpass` method allows authentication using a username/password stored in Vault. The `kubernetes` method allows authentication for a Service Account coming from the Kubernetes cluster configured in the method.
* Each Kubernetes/Openshift cluster (Cloud Edge) will be configured for authentication using the `kubernetes` authentication method, allowing Service Accounts from each edge to use Vault.
* https://learn.hashicorp.com/vault/getting-started/authentication
---
### Policies
*  Govern the behavior of clients and instrument Role-Based Access Control (RBAC) by specifying access privileges (authorization).
* When an entity authenticates to Vault it uses a time limited auto generated token. This token is granted permissions by the policies that are assigned to it, defined by the authentication method roles.
* Each project will have two policies - one granting full control over the project's secret engine and the other granting only `read` permissions to the project's secrets. The former policy will be assigned to the user that is used to manage the secrets (via UI/API) while the latter will be assigned to the project's Service Account from each Kubernetes cluster, in order for it to read secrets from Vault and create Kubernetes secrets from them.
* https://learn.hashicorp.com/vault?track=identity-access-management#identity-access-management
---
## Read more
* [https://www.vaultproject.io/docs](https://www.vaultproject.io/docs)
* [https://learn.hashicorp.com/vault](https://learn.hashicorp.com/vault)
* [https://github.com/godaddy/kubernetes-external-secrets](https://github.com/godaddy/kubernetes-external-secrets)
