from app.memory.store import ConversationStore

def test_conversation_roundtrip(tmp_path):
    store = ConversationStore(str(tmp_path / "test.db"))
    store.add("u1","c1","user","Hello")
    store.add("u1","c1","assistant","Hi")
    assert [m["role"] for m in store.history("u1","c1")] == ["user","assistant"]
    store.clear("u1","c1")
    assert store.history("u1","c1") == []
