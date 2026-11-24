struct Record0 {
	labels []string
}

fn main() {
	first := Record0{
		labels: [
			'owned',
		],
	}
	my_data := first
	_ = my_data
}
