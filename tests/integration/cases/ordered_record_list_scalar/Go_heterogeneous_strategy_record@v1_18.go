package main
type Record0 struct {
	Id int
}

func main() {
my_data := [][2]any{
	{"first", []Record0{Record0{Id: 1}}},
	{"second", 2},
}
_ = my_data
}
