struct Record0 {
	flags []bool
	values []f64
	ints []int
	text []string
	nested_flags [][]bool
	nested_values [][]f64
}

fn main() {
	my_data := Record0{
		flags: [
			true,
			false,
		],
		values: [
			1.5,
			-2.25,
		],
		ints: [
			1,
			2,
		],
		text: [
			'a',
		],
		nested_flags: [
			[
				true,
			],
			[
				false,
			],
		],
		nested_values: [
			[
				1.5,
			],
			[
				2.25,
			],
		],
	}
	_ = my_data
}
