package main
type Record0 struct {
	Value int
}
func consume(args ...any) any { return nil }

func main() {
item := Record0{
	Value: 1,
}
consume(item)
}
