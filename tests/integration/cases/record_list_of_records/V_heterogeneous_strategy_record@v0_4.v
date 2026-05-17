struct Record1 {
	id int
	label string
}
struct Record0 {
	name string
	items []Record1
}

fn main() {
	my_data := Record0{
		name: 'box',
		items: [
			Record1{
				id: 1,
				label: 'first',
			},
			Record1{
				id: 2,
				label: 'second',
			},
		],
	}
	_ = my_data
}
