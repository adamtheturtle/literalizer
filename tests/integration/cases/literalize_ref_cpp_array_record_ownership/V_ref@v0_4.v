struct Record1 {
	values []int
}
struct Record2 {
	nested [][]int
}
struct Record0 {
	trivial Record1
	nested Record2
}

fn main() {
	trivial := Record1{
		values: [
			1,
			2,
		],
	}
	nested := Record2{
		nested: [
			[
				1,
				2,
			],
			[
				3,
				4,
			],
		],
	}
	my_data := Record0{
		trivial: trivial,
		nested: nested,
	}
	_ = my_data
}
