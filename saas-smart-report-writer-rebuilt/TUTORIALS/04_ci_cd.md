# CI/CD with GitHub Actions

- Workflow runs tests (API unit tests) and builds docker images.
- Extend with push to registry using `docker/login-action` + `docker/build-push-action`.
- Add more tests under `tests/`.
