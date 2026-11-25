package main

func main() {
my_data := map[string][]map[string]any{
	"divergent": []map[string]any{{"b": 1}, {"a": "hello"}},
	"matching": []map[string]any{{"n": 1}, {"n": 2}},
}
_ = my_data
}
