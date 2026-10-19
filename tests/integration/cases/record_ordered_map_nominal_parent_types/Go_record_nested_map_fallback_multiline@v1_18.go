package main
type Record2 struct {
	X int
}
type Record1 struct {
	Values [][2]any
	Flag bool
}
type Record3 struct {
	Y string
}
type Record0 struct {
	First Record1
	Second Record1
}

func main() {
my_data := Record0{
	First: Record1{
		Values: [][2]any{
			{"item", Record2{
				X: 1,
			}},
		},
		Flag: true,
	},
	Second: Record1{
		Values: [][2]any{
			{"item", Record3{
				Y: "s",
			}},
		},
		Flag: false,
	},
}
_ = my_data
}
