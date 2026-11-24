struct Record0 {
	numbers []int
	nested_numbers [][]int
	words []string
	flag bool
}

fn main() {
	my_data := Record0{
		numbers: [
			1,
			2,
		],
		nested_numbers: [
			[
				3,
				4,
			],
			[
				5,
				6,
			],
		],
		words: [
			's',
		],
		flag: true,
	}
	_ = my_data
}
