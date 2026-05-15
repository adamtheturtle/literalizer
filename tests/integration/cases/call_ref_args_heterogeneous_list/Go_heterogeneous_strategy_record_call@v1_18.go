package main
func process(args ...any) any { return nil }

func main() {
my_ints := []int{
	1,
	2,
	3,
}
my_strings := []string{
	"a",
	"b",
}
my_empty := []any{}
process(my_ints, 42)
process(my_strings, 7)
process(my_empty, 99)
}
