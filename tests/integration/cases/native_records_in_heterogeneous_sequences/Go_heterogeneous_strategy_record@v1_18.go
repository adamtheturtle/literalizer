package main
type Record1 struct {
	K []bool
}
type Record0 struct {
	H []any
}

func main() {
my_data := Record0{
	H: []any{
		1,
		"a",
		[]any{
			2,
			"b",
		},
		Record1{
			K: []bool{
				true,
			},
		},
	},
}
_ = my_data
}
