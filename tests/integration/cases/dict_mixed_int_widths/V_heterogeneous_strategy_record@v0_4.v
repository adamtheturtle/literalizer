struct Record0 {
	a int
	b i64
	c string
}

fn main() {
	my_data := Record0{
		a: 1,
		b: i64(3000000000),
		c: 'x',
	}
	_ = my_data
}
