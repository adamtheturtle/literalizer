package main

func main() {
item_var := map[string]string{
	"_": "_",
}
my_data := map[string][]map[string]string{
	"items": []map[string]string{item_var, {"fallback": "value"}},
}
_ = my_data
}
