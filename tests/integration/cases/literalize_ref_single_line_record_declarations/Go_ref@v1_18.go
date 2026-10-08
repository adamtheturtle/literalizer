package main
type Record1 struct {
	X string
}
type Record2 struct {
	X int
}
type Record0 struct {
	Direct Record1
	Bound Record2
}

func main() {
First := Record2{
	X: 1,
}
my_data := Record0{
	Direct: Record1{
		X: "s",
	},
	Bound: First,
}
_ = my_data
}
