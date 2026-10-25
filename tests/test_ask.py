from types import SimpleNamespace

from app import ask


class FakeChat:
    def __init__(self):
        self.messages = []
        self.configs = []

    def send_message(self, message, config=None):
        self.messages.append(message)
        self.configs.append(config)
        return SimpleNamespace(
            text=f"answer: {message}",
            usage_metadata=SimpleNamespace(
                prompt_token_count=3,
                candidates_token_count=5,
            ),
        )


def test_main_keeps_chat_for_follow_up_questions(monkeypatch, capsys):
    chat = FakeChat()
    created_models = []

    class FakeChats:
        def create(self, *, model):
            created_models.append(model)
            return chat

    class FakeClient:
        def __init__(self, *, api_key):
            assert api_key == "test-key"
            self.chats = FakeChats()

    questions = iter(["second question", ""])
    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(
        "sys.argv", ["app.ask", "--temperature", "0.2", "first question"]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(questions))

    ask.main()

    output = capsys.readouterr().out
    assert chat.messages == ["first question", "second question"]
    assert [config.temperature for config in chat.configs] == [0.2, 0.2]
    assert created_models == [ask.MODEL]
    assert "answer: first question" in output
    assert "answer: second question" in output
    assert output.count("[tokens] input=3 output=5") == 2
