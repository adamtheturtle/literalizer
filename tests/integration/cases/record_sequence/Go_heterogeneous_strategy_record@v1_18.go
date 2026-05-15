package main
type Record0 struct {
	Id int
	Label string
	Tags []any
}

func main() {
my_data := []any{
	Record0{Id: 1, Label: "first", Tags: []any{}},
	Record0{Id: 2, Label: "second", Tags: []any{}},
	Record0{Id: 3, Label: "third", Tags: []any{}},
}
_ = my_data
}
