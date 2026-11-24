package main
type Record0 struct {
	Call string
	Args []any
}

func main() {
my_data := Record0{
	Call: "send",
	Args: []any{
		1,
		"email",
		"a@gmail.com",
		100,
	},
}
_ = my_data
}
