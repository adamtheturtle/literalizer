package main

func main() {
A := map[string]any{
	"k": "s",
}
my_data := []map[string]any{
	A,
	{"k": 1},
}
_ = my_data
}
