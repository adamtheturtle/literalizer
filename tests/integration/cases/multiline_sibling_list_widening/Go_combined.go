package main

func main() {
my_data := map[string]any{
	"sibling_lists": map[string]any{"numbers": []any{1, 2}, "strings": []any{"x", "y"}},
	"ref_marker_present": []string{"$keep", "z"},
}
my_data = map[string]any{
	"sibling_lists": map[string]any{"numbers": []any{1, 2}, "strings": []any{"x", "y"}},
	"ref_marker_present": []string{"$keep", "z"},
}
_ = my_data
}
