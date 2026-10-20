struct Record0 {
	x int
	y voidptr
}

fn main() {
	value := Record0{
		x: 1,
		y: unsafe { nil },
	}
	my_data := value
	_ = my_data
}
