package main

func main() {
my_data := map[string]any{
    "level1": map[string]any{"level2": map[string]any{"level3": map[string]any{"level4": map[string]any{"value": "deep", "items": []any{"a", "b"}}}, "sibling": 42}, "tags": []any{map[string]any{"name": "tag1", "meta": map[string]any{"priority": 1, "labels": []any{"x", "y"}}}}},
}
_ = my_data
}
