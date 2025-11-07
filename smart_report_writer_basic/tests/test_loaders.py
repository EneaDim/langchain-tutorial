def test_imports():
    import smart_report_writer.loaders.files as f
    assert callable(f.load_any)
