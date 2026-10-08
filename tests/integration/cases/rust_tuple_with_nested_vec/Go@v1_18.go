package main

func main() {
my_data := map[string]any{
	"lint": []any{2, []any{}},
	"test": []any{5, []string{"compile"}},
	"package": []any{7, []string{"link", "test"}},
}
_ = my_data
}
