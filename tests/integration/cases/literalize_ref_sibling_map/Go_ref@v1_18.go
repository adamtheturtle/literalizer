package main

func main() {
SiblingMap := map[string]int{
	"k": 2,
}
my_data := []map[string]int{
	{"k": 1},
	SiblingMap,
}
_ = my_data
}
