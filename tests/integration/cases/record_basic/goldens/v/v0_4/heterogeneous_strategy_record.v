struct Record0 {
	id int
	label string
	enabled bool
	related_ids []int
}

fn main() {
	my_data := Record0{
		id: 1,
		label: 'She said "hello", then waved',
		enabled: false,
		related_ids: [
			1,
			2,
			3,
		],
	}
	_ = my_data
}
