def test_prompts_import():
    from smart_report_writer import prompts
    assert hasattr(prompts, "DOC_SUMMARY_PROMPT")
