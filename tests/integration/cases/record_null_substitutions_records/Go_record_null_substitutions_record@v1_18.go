package main
type Record0 struct {
	DueDate int
	ParentId int
	Assignee string
}

func main() {
my_data := []any{
	Record0{DueDate: -1, ParentId: -1, Assignee: ""},
	Record0{DueDate: 10, ParentId: 20, Assignee: "alice"},
}
_ = my_data
}
