def test_main_output(capsys):
    from src.main import main
    main()
    captured = capsys.readouterr()
    assert "Hello from snoop" in captured.out
