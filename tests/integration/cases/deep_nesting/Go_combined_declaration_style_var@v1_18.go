package main

func main() {
var my_data = map[string]map[string]any{
	"level1": map[string]any{"level2": map[string]any{"level3": map[string]map[string]any{"level4": map[string]any{"value": "deep", "items": []string{"a", "b"}}}, "sibling": 42}, "tags": []map[string]any{{"name": "tag1", "meta": map[string]any{"priority": 1, "labels": []string{"x", "y"}}}}},
}
my_data = map[string]map[string]any{
	"level1": map[string]any{"level2": map[string]any{"level3": map[string]map[string]any{"level4": map[string]any{"value": "deep", "items": []string{"a", "b"}}}, "sibling": 42}, "tags": []map[string]any{{"name": "tag1", "meta": map[string]any{"priority": 1, "labels": []string{"x", "y"}}}}},
}
_ = my_data
}
