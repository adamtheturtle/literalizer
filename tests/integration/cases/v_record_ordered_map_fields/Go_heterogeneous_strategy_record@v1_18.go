package main
type Record0 struct {
	Numbers [][2]any
	Words [][2]any
	Nested [][2]any
	Empty [][2]any
	Flag bool
	NestedMaps [][2]any
	EmptyNestedMaps [][2]any
}

func main() {
my_data := Record0{
	Numbers: [][2]any{
		{"first", 1},
	},
	Words: [][2]any{
		{"first", "s"},
	},
	Nested: [][2]any{
		{"first", []int{
			1,
			2,
		}},
	},
	Empty: [][2]any{},
	Flag: true,
	NestedMaps: [][2]any{
		{"first", [][2]any{
			{"nested", 1},
		}},
	},
	EmptyNestedMaps: [][2]any{
		{"first", [][2]any{}},
	},
}
_ = my_data
}
