package main
type Record0 struct {
	Id int
	Description string
	IsDone bool
	Blocks []int
}

func main() {
my_data := Record0{
	Id: 1,
	Description: "She said \"hello\", then waved",
	IsDone: false,
	Blocks: []int{
		1,
		2,
		3,
	},
}
_ = my_data
}
