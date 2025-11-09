# 🔄 CI — Docker *Build & Start* Only (GitHub Actions)

This document shows a **minimal** CI workflow that does just two things on every push:

1) **Build** your Docker images with `docker compose build`  
2) **Start** your stack in the GitHub runner with `docker compose up -d`

No tests, no publishing, no deploy — strictly **build & start**.

---

## 1) Why run Compose in CI?

- Validate Dockerfiles build successfully on a clean machine.
- Validate that services **start** together (basic integration sanity).
- Keep the pipeline fast and simple.

> Note: Ports exposed by Compose are reachable **inside the runner only**. This job is not for public access or deploy.

---

## 2) Minimal Workflow (copy/paste into your repo)

Create `.github/workflows/ci-docker-build-start.yml` with the following content:

```yaml
name: Docker Build & Start

on:
  push:
    branches: ["**"]   # run on every branch
  pull_request:

jobs:
  build_and_start:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      # Optional: speed up multi-arch or layer caching in future
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build images
        run: |
          docker compose version
          docker compose build --pull

      - name: Start stack
        run: |
          docker compose up -d
          docker compose ps

      # (Optional) Quick internal sanity check — keep commented if you truly want only build & start
      # - name: Sanity check (internal)
      #   run: |
      #     sleep 8
      #     curl -sf http://localhost:8000/healthz || (docker compose logs backend; exit 1)
      #     curl -sf http://localhost:8502/_stcore/health || true

      # Always tear down to free runner resources
      - name: Stop stack
        if: always()
        run: docker compose down -v
```

What it does

- Build images: docker compose build --pull
- Start stack: docker compose up -d
- Tear down: docker compose down -v (even if previous steps fail)

The commented “Sanity check” step is optional; leave it commented if you want strictly build & start.

## 3) Local parity (optional)

To mirror the CI steps locally:

```bash
docker compose build --pull
docker compose up -d
docker compose ps
docker compose down -v
```

## 4) Notes & Tips

- This workflow assumes your docker-compose.yml at repo root is valid and self-contained.
- If your UI port is mapped to 8502 and backend to 8000, you can curl them from the runner (but again, it’s not exposed outside).
- Keep secrets out of this job; it’s meant for quick validation, not deploy.

