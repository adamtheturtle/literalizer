struct Record1 {
	a int
	b string
	c voidptr
}
struct Record0 {
	outer Record1
}

fn main() {
	my_data := Record0{
		outer: Record1{
			a: 1,
			b: 'x',
			c: unsafe { nil },
		},
	}
	_ = my_data
}
