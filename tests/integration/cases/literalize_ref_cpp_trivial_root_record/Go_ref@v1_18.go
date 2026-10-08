package main
type Record1 struct {
	Value int
}
type Record0 struct {
	Child Record1
}

func main() {
First := Record0{
	Child: Record1{
		Value: 1,
	},
}
my_data := First
_ = my_data
}
