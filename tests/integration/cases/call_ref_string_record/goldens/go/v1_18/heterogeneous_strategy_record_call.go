package main
type Record0 struct {
	Value string
}
func consume(args ...any) any { return nil }

func main() {
item := Record0{
	Value: "owned",
}
consume(item)
}
