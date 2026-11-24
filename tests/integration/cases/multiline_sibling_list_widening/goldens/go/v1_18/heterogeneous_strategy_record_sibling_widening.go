package main
type Record1 struct {
	Numbers []int
	Strings []string
}
type Record0 struct {
	OmapValue [][2]any
	SiblingLists Record1
	RefMarkerPresent []string
}

func main() {
my_data := Record0{
	OmapValue: [][2]any{
		{"first", 1},
	},
	SiblingLists: Record1{
		Numbers: []int{
			1,
			2,
		},
		Strings: []string{
			"x",
			"y",
		},
	},
	RefMarkerPresent: []string{
		"$keep",
		"z",
	},
}
_ = my_data
}
