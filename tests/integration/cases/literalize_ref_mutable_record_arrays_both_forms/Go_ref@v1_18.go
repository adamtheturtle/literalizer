package main
type Record0 struct {
	Id int
}

func main() {
var Shared = []Record0{
	Record0{Id: 1},
}
var Second = []Record0{
	Record0{Id: 2},
}
var my_data = [][]Record0{
	Shared,
	Second,
}
my_data = [][]Record0{
	Shared,
	Second,
}
_ = my_data
}
