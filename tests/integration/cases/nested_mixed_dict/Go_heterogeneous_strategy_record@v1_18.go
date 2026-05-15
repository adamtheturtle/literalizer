package main
type Record1 struct {
	A int
	B string
	C any
}
type Record0 struct {
	Outer Record1
}

func main() {
my_data := Record0{
	Outer: Record1{
		A: 1,
		B: "x",
		C: nil,
	},
}
_ = my_data
}
