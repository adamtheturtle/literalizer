package main
type Record1 struct {
	X int
}
type Record0 struct {
	Values [][2]any
	Flag bool
}

func main() {
my_data := Record0{
	Values: [][2]any{
		{"entries", []any{
			[][2]any{
				{"inner", Record1{
					X: 1,
				}},
			},
			[][2]any{
				{"inner", Record1{
					X: 2,
				}},
			},
		}},
	},
	Flag: true,
}
_ = my_data
}
