package main
type Record1 struct {
	Id int
	Label string
}
type Record0 struct {
	Name string
	Items []Record1
}

func main() {
my_data := Record0{
	Name: "box",
	Items: []Record1{
		Record1{
			Id: 1,
			Label: "first",
		},
		Record1{
			Id: 2,
			Label: "second",
		},
	},
}
_ = my_data
}
