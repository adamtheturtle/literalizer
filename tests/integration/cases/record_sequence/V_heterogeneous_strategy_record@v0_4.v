interface IVal {}
struct Record0 {
	id int
	label string
	tags []IVal
}

fn main() {
	my_data := [
		Record0{ id: 1, label: 'first', tags: []IVal{} },
		Record0{ id: 2, label: 'second', tags: []IVal{} },
		Record0{ id: 3, label: 'third', tags: []IVal{} },
	]
	_ = my_data
}
