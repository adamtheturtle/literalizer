package main
type Record0 struct {
	Scores []int
	Args []any
}

func main() {
my_data := Record0{
	Scores: []int{
		10,
		20,
		30,
	},
	Args: []any{
		1,
		"email",
		"a@gmail.com",
		100,
	},
}
_ = my_data
}
