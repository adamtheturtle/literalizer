package main

func main() {
Foo := map[string]string{
	"_": "_",
}
my_data := map[string]any{
	"items": []map[string]int{{"other": 1}, Foo},
	"mapping": map[string]map[string]string{"value": Foo},
}
_ = my_data
}
