package main
type Record2 struct {
	Value int
}
type Record1 struct {
	Items []any
}
type Record3 struct {
	Value string
}
type Record0 struct {
	First Record1
	Second Record1
}

func main() {
my_data := Record0{
	First: Record1{
		Items: []any{
			1,
			Record2{
				Value: 2,
			},
		},
	},
	Second: Record1{
		Items: []any{
			1,
			Record3{
				Value: "s",
			},
		},
	},
}
_ = my_data
}
