from app.tasks import analyze_pr_task

def test_analyze_pr_task(mocker):
    mocker.patch("app.utils.fetch_pr_diff", return_value="mock_diff")
    mocker.patch("app.utils.analyze_code", return_value={"mock": "results"})
    
    result = analyze_pr_task("mock_task_id", {"repo_url": "url", "pr_number": 123})
    assert result == {"mock": "results"}
