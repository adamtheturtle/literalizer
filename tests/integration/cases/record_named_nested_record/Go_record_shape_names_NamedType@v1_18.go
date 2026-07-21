package main
type NamedType struct {
	Id int
	Description string
	IsDone bool
	Blocks []int
}
type Record0 struct {
	Project string
	LeadTask NamedType
}

func main() {
my_data := Record0{
	Project: "alpha",
	LeadTask: NamedType{
		Id: 100,
		Description: "first task",
		IsDone: false,
		Blocks: []int{
			102,
			103,
		},
	},
}
_ = my_data
}
