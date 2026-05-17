struct Record0 {
	a int
	b string
}

fn main() {
	mut my_data := Record0{
		a: 1,
		b: 'x',
	}
	my_data = Record0{
		a: 1,
		b: 'x',
	}
	_ = my_data
}
