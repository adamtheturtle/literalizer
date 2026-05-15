package main
type Record0 struct {
	Title string
	Tags []string
	Priority int
}

func main() {
my_data := Record0{
	Title: "report",
	Tags: []string{
		"draft",
		"urgent",
		"review",
	},
	Priority: 2,
}
_ = my_data
}
