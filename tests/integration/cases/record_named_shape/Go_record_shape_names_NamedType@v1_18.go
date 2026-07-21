package main
type NamedType struct {
	Id int
	Description string
	IsDone bool
	Blocks []int
}

func main() {
my_data := []any{
	NamedType{Id: 100, Description: "first task", IsDone: false, Blocks: []int{102, 103}},
	NamedType{Id: 101, Description: "second task", IsDone: true, Blocks: []int{100}},
}
_ = my_data
}
