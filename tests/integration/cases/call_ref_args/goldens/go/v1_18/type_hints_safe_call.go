package main
func process(args ...any) any { return nil }

func main() {
my_var := []int{
	1,
	2,
	3,
}
my_other := []int{
	4,
	5,
	6,
}
process(my_var, 42)
process(my_other, 7)
}
