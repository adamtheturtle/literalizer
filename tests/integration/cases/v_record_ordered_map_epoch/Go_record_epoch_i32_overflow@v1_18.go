package main
type Record0 struct {
	Values [][2]any
	Flag bool
	NestedValues [][2]any
	ListValues [][2]any
}

func main() {
my_data := Record0{
	Values: [][2]any{
		{"first", 2208988800},
	},
	Flag: true,
	NestedValues: [][2]any{
		{"first", [][2]any{
			{"nested", 2208988800},
		}},
	},
	ListValues: [][2]any{
		{"first", []int{
			2208988800,
		}},
	},
}
_ = my_data
}
