void _declaration() {
  final my_data = {
      "level1": {"level2": {"level3": {"level4": {"value": "deep", "items": <String>["a", "b"]}}, "sibling": 42}, "tags": [{"name": "tag1", "meta": {"priority": 1, "labels": <String>["x", "y"]}}]},
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = {
      "level1": {"level2": {"level3": {"level4": {"value": "deep", "items": <String>["a", "b"]}}, "sibling": 42}, "tags": [{"name": "tag1", "meta": {"priority": 1, "labels": <String>["x", "y"]}}]},
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
