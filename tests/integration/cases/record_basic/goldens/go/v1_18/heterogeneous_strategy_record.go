package main
type Record0 struct {
	Id int
	Label string
	Enabled bool
	RelatedIds []int
}

func main() {
my_data := Record0{
	Id: 1,
	Label: "She said \"hello\", then waved",
	Enabled: false,
	RelatedIds: []int{
		1,
		2,
		3,
	},
}
_ = my_data
}
