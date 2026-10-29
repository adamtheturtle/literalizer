package main
func f(args ...any) any { return nil }

func main() {
ref_data := []int{
	1,
	2,
}
f([][]int{
	ref_data,
})
f([][]int{
	ref_data,
})
}
