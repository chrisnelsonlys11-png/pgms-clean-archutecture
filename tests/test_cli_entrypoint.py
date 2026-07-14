from app.presentation.cli.main import main


def test_cli_main_runs_without_starting_fastapi(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "0")

    main()

    captured = capsys.readouterr()
    assert "PGMS CLI" in captured.out
    assert "Goodbye" in captured.out
