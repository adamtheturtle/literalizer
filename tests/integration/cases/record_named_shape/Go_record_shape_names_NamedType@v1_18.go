package main
type NamedType struct {
	Id int
	Label string
	Enabled bool
	RelatedIds []int
}

func main() {
my_data := []any{
	NamedType{Id: 100, Label: "first entry", Enabled: false, RelatedIds: []int{102, 103}},
	NamedType{Id: 101, Label: "second entry", Enabled: true, RelatedIds: []int{100}},
}
_ = my_data
}
