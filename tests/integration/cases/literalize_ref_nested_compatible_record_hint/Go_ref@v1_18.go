package main
type Record1 struct {
	Items []int
}
type Record0 struct {
	Outer Record1
}

func main() {
RecordData := Record1{
	Items: []int{
		1,
		2,
	},
}
my_data := Record0{
	Outer: RecordData,
}
_ = my_data
}
