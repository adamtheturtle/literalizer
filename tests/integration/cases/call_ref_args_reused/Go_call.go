package main
func process(args ...any) any { return nil }

func main() {
single_var := []int{
	4,
	5,
	6,
}
repeated_var := 1
process(repeated_var, 1);
process(single_var, 0);
process(repeated_var, 8);
}
