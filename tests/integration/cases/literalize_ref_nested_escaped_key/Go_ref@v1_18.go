package main

func main() {
Foo := map[string]string{
	"_": "_",
}
my_data := map[string]any{
	"mapping": map[string]map[string]string{"value": Foo},
	"items": []map[string]int{{"other": 1}, Foo},
}
_ = my_data
}
