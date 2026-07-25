package main
type NamedType struct {
	Id int
	Label string
	Enabled bool
	RelatedIds []int
}
type Record0 struct {
	Collection string
	FeaturedEntry NamedType
}

func main() {
my_data := Record0{
	Collection: "alpha",
	FeaturedEntry: NamedType{
		Id: 100,
		Label: "first entry",
		Enabled: false,
		RelatedIds: []int{
			102,
			103,
		},
	},
}
_ = my_data
}
