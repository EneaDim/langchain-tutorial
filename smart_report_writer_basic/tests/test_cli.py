def test_cli_import():
    import smart_report_writer.cli as cli
    assert hasattr(cli, "main")
