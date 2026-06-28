from arcgis_project.content import search_items, summarize_item, summarize_items


class _FakeItem:
    def __init__(self, id, title, type="Feature Service", owner="alice", numViews=3):
        self.id = id
        self.title = title
        self.type = type
        self.owner = owner
        self.numViews = numViews


class _FakeContent:
    def __init__(self, items):
        self._items = items
        self.last_call = None

    def search(self, query="", item_type=None, max_items=10):
        self.last_call = {"query": query, "item_type": item_type, "max_items": max_items}
        return self._items[:max_items]


class _FakeGIS:
    def __init__(self, items):
        self.content = _FakeContent(items)


def test_search_items_passes_args_through():
    gis = _FakeGIS([_FakeItem("1", "A"), _FakeItem("2", "B")])
    result = search_items(gis, query="owner:me", item_type="Web Map", max_items=1)
    assert len(result) == 1
    assert gis.content.last_call == {
        "query": "owner:me",
        "item_type": "Web Map",
        "max_items": 1,
    }


def test_summarize_item():
    summary = summarize_item(_FakeItem("abc", "Roads"))
    assert summary == {
        "id": "abc",
        "title": "Roads",
        "type": "Feature Service",
        "owner": "alice",
        "num_views": 3,
    }


def test_summarize_items():
    items = [_FakeItem("1", "A"), _FakeItem("2", "B")]
    assert [s["id"] for s in summarize_items(items)] == ["1", "2"]
