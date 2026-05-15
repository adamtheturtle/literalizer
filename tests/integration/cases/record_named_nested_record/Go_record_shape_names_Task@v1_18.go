package main
type Task struct {
	Id int
	Description string
	IsDone bool
	Blocks []int
}
type Record0 struct {
	Project string
	LeadTask Task
}

func main() {
my_data := Record0{
	Project: "alpha",
	LeadTask: Task{
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
