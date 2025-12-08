## Infrastructure

Resources are stored/deployed to GCP and managed with terraform.

**Please avoid creating resrouces manually**. Prefer defining them here.

See [documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs).

### Rollback

```
gcloud run revisions list --service=rag-service --region=europe-west10
# "=100" for 100% traffic
gcloud run services update-traffic rag-service \
  --to-revisions=rag-service-00001-abc=100 \
  --region=europe-west10
```
