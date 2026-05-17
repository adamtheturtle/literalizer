struct Record0 {
	id int
	description string
	is_done bool
	blocks []int
}

fn main() {
	my_data := Record0{
		id: 1,
		description: 'She said "hello", then waved',
		is_done: false,
		blocks: [
			1,
			2,
			3,
		],
	}
	_ = my_data
}
