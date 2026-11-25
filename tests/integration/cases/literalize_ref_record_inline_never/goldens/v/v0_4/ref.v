struct Record0 {
	x int
	y voidptr
}

fn main() {
	my_data := Record0{
		x: 1,
		y: unsafe { nil },
	}
	_ = my_data
}
