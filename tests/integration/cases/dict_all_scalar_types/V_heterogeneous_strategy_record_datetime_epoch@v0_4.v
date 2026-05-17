struct Record0 {
	s string
	i int
	f f64
	b bool
	n voidptr
	d string
	dt int
	by string
}

fn main() {
	my_data := Record0{
		s: 'string',
		i: 1,
		f: 1.5,
		b: true,
		n: unsafe { nil },
		d: "2024-01-15",
		dt: 1705320000,
		by: "48656c6c6f",
	}
	_ = my_data
}
