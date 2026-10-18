interface IVal {}
struct Record0 {
	a [][]int
	b [][]int
}

fn main() {
	my_data := Record0{
		a: [
			[
				1,
				2,
			],
			[
				3,
			],
		],
		b: [
			[]int{},
			[
				1,
			],
		],
	}
	_ = my_data
}
