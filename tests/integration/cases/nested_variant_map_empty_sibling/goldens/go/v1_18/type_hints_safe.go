package main

func main() {
my_data := []map[string]map[string]any{
	{"nested": map[string]any{"count": 1, "name": "value"}},
	{},
}
_ = my_data
}
