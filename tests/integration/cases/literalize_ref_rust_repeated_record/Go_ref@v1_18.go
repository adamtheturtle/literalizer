package main
type Record0 struct {
	Value []int
}

func main() {
Shared := Record0{
	Value: []int{
		1,
		2,
	},
}
my_data := []Record0{
	Shared,
	Shared,
}
_ = my_data
}
