package main
func f(args ...any) any { return nil }

func main() {
x := [][]int{
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
		x,
	},
})
}
