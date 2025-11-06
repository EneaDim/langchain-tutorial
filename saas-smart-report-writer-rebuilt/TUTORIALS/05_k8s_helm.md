# Kubernetes via Helm

1. Build and push your image.
2. Set `image.repository` & `tag` in `values.yaml`.
3. `helm install srw ./infra/helm -n srw --create-namespace`
4. Configure ingress if needed.
5. Manage secrets with Kubernetes Secrets or external secret manager (S3 keys, DB creds).
