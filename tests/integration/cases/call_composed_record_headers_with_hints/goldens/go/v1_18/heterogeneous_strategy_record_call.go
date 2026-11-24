package main
type Record0 struct {
	Name string
	Values []int
}
func consume(args ...any) any { return nil }

func main() {
item := Record0{
	Name: "first",
	Values: []int{
		1,
		2,
	},
}
consume(item)
}
