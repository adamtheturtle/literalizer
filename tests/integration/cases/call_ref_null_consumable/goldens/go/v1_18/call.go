package main
func consume(args ...any) any { return nil }

func main() {
var my_null any = nil
var regular_null any = nil
consume(my_null)
consume(regular_null)
}
