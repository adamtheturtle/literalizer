package main

func main() {
Std := map[string]int{
	"a": 1,
}
Arena := map[string]int{
	"a": 1,
}
Allocator := map[string]int{
	"a": 1,
}
my_data := []map[string]int{
	Std,
	Arena,
	Allocator,
}
_ = my_data
}
