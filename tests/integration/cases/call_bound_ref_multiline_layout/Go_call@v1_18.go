package main
func f(args ...any) any { return nil }

func main() {
ref_data := [][]int{
	[]int{
		1,
		2,
	},
	[]int{
		3,
		4,
	},
}
f([][][][]int{
	[][][]int{
		ref_data,
	},
})
}
