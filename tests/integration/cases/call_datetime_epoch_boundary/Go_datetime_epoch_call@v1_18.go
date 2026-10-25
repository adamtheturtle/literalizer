package main
func consume(args ...any) any { return nil }

func main() {
consume(-2147483649)
consume(2147483648)
}
