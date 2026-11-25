package main

func main() {
my_data := map[string]any{
	"omap_value": [][2]any{{"first", 1}},
	"sibling_lists": map[string]any{"numbers": []any{1, 2}, "strings": []any{"x", "y"}},
	"ref_marker_present": []string{"$keep", "z"},
}
_ = my_data
}
