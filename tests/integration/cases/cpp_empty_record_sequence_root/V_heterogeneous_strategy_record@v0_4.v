interface IVal {}
struct Record0 {
	x int
}

fn main() {
	my_data := [
		[]Record0{},
		[Record0{ x: 1 }],
	]
	_ = my_data
}
