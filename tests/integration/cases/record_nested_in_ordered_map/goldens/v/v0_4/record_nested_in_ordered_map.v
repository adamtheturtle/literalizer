struct Record0 {
	name voidptr
	id int
}

fn main() {
	my_data := {
		'outer': [Record0{ name: unsafe { nil }, id: 1 }],
	}
	_ = my_data
}
