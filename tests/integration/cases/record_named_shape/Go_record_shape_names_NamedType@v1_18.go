package main
type NamedType struct {
	Id int
	Label string
	Enabled bool
	RelatedIds []int
}

func main() {
my_data := []any{
	NamedType{Id: 100, Label: "first item", Enabled: false, RelatedIds: []int{102, 103}},
	NamedType{Id: 101, Label: "second item", Enabled: true, RelatedIds: []int{100}},
}
_ = my_data
}
