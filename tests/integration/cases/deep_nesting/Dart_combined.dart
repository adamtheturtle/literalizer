void main() {
  {
    final my_data = {
        "level1": {"level2": {"level3": {"level4": {"value": "deep", "items": <String>["a", "b"]}}, "sibling": 42}, "tags": [{"name": "tag1", "meta": {"priority": 1, "labels": <String>["x", "y"]}}]},
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = {
        "level1": {"level2": {"level3": {"level4": {"value": "deep", "items": <String>["a", "b"]}}, "sibling": 42}, "tags": [{"name": "tag1", "meta": {"priority": 1, "labels": <String>["x", "y"]}}]},
    };
    my_data.hashCode;
  }
}
