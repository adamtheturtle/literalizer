package main
type Record0 struct {
	Quantity int
	Big uint64
	Ratio float64
	Label string
	Ok bool
}

func main() {
my_data := Record0{
	Quantity: 0xf4240,
	Big: uint64(18446744073709551615),
	Ratio: 2.5,
	Label: "tag",
	Ok: true,
}
_ = my_data
}
