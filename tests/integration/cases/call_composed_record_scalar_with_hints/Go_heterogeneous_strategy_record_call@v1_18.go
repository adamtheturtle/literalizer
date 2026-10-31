package main
type Record0 struct {
	A int
}
func consume(args ...any) any { return nil }

func main() {
item := Record0{
	A: 1,
}
consume(item)
}
