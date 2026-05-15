package main
type Record0 struct {
	Id int
	Label string
}

func main() {
my_data := []any{
	Record0{Id: 1, Label: "first"},
	Record0{Id: 2, Label: "second"},
	Record0{Id: 3, Label: "third"},
}
_ = my_data
}
