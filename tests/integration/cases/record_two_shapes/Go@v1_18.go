package main

func main() {
my_data := map[string]map[string]any{
	"user": map[string]any{"id": 1, "name": "Alice"},
	"project": map[string]any{"title": "report", "tags": []string{"draft", "urgent"}},
}
_ = my_data
}
