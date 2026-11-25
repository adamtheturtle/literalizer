package main

func main() {
StringMap := map[string]any{
	"k": "s",
}
my_data := []map[string]any{
	StringMap,
	{"k": 1},
}
_ = my_data
}
