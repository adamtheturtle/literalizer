package main

func main() {
Actual := map[string]any{
	"_": "_",
}
my_data := []map[string]any{
	{"$ref": 1},
	{"$ref": nil},
	Actual,
}
_ = my_data
}
