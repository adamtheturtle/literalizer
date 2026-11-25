package main
type Record0 struct {
	A [][]int
	B [][]int
}

func main() {
my_data := Record0{
	A: [][]int{
		[]int{
			1,
			2,
		},
		[]int{
			3,
		},
	},
	B: [][]int{
		[]int{},
		[]int{
			1,
		},
	},
}
_ = my_data
}
