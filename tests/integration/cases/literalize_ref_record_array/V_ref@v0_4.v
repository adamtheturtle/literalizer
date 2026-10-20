struct Record0 {
	x int
}

fn main() {
	first := [
		Record0{ x: 1 },
		Record0{ x: 2 },
	]
	my_data := first.clone()
	_ = my_data
}
