struct Record0 {
	title string
	tags []string
	priority int
}

fn main() {
	my_data := Record0{
		title: 'report',
		tags: [
			'draft',
			'urgent',
			'review',
		],
		priority: 2,
	}
	_ = my_data
}
