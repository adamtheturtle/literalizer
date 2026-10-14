package main
type Record0 struct {
	Id int
}

func main() {
Shared := []Record0{
	Record0{Id: 1},
}
Second := []Record0{
	Record0{Id: 2},
}
my_data := [][]Record0{
	Shared,
	Second,
}
my_data = [][]Record0{
	Shared,
	Second,
}
_ = my_data
}
