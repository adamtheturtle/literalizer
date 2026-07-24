package main
type NamedType struct {
	Id int
	Label string
	Enabled bool
	RelatedIds []int
}
type Record0 struct {
	Project string
	LeadItem NamedType
}

func main() {
my_data := Record0{
	Project: "alpha",
	LeadItem: NamedType{
		Id: 100,
		Label: "first item",
		Enabled: false,
		RelatedIds: []int{
			102,
			103,
		},
	},
}
_ = my_data
}
