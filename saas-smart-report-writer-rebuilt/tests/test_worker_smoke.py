def test_dummy_worker_smoke():
    import api.workers.tasks as t
    assert hasattr(t, "run_summarize_pipeline")
