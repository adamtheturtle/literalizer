package main
type Record0 struct {
	Values [][2]any
	Flag bool
	DirectArrays [][]int64
}

func main() {
my_data := Record0{
	Values: [][2]any{
		{"wide", []any{
			[]int64{
				2208988800,
			},
			[]int64{},
		}},
		{"narrow", []any{
			[]int{
				946684800,
			},
		}},
		{"negative", []any{
			[]int64{
				-2208988800,
			},
		}},
		{"shifted", []any{
			[]int64{
				2208988800,
			},
		}},
		{"mixed_width", []any{
			[]int{
				946684800,
			},
			[]int64{
				2208988800,
			},
		}},
		{"text", "preserve"},
	},
	Flag: true,
	DirectArrays: [][]int64{
		[]int64{
			2208988800,
		},
		[]int64{},
	},
}
_ = my_data
}
