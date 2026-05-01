package main

func main() {
my_var := map[string]string{
	"_": "_",
}
item_var := map[string]string{
	"_": "_",
}
my_data := map[string]any{
	"key": my_var,
	"items": []map[string]string{item_var, {"fallback": "value"}},
}
_ = my_data
}
