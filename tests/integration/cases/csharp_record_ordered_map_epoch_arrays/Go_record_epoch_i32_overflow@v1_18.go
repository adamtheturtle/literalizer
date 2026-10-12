package main
type Record0 struct {
	Values [][2]any
	Flag bool
	DirectArrays [][]int
}

func main() {
my_data := Record0{
	Values: [][2]any{
		{"wide", [][]int{
			[]int{
				2208988800,
			},
			[]int{},
		}},
		{"narrow", [][]int{
			[]int{
				946684800,
			},
		}},
		{"negative", [][]int{
			[]int{
				-2208988800,
			},
		}},
		{"shifted", [][]int{
			[]int{
				2208988800,
			},
		}},
		{"mixed_width", [][]int{
			[]int{
				946684800,
			},
			[]int{
				2208988800,
			},
		}},
		{"text", "preserve"},
	},
	Flag: true,
	DirectArrays: [][]int{
		[]int{
			2208988800,
		},
		[]int{},
	},
}
_ = my_data
}
