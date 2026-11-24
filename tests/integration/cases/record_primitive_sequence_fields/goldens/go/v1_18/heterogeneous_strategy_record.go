package main
type Record0 struct {
	Flags []bool
	Values []float64
	Ints []int
	Text []string
	NestedFlags [][]bool
	NestedValues [][]float64
}

func main() {
my_data := Record0{
	Flags: []bool{
		true,
		false,
	},
	Values: []float64{
		1.5,
		-2.25,
	},
	Ints: []int{
		1,
		2,
	},
	Text: []string{
		"a",
	},
	NestedFlags: [][]bool{
		[]bool{
			true,
		},
		[]bool{
			false,
		},
	},
	NestedValues: [][]float64{
		[]float64{
			1.5,
		},
		[]float64{
			2.25,
		},
	},
}
_ = my_data
}
