struct Record0 {
	value i64
}

fn main() {
	my_data := Record0{
		value: i64(-0x8000000000000000),
	}
	_ = my_data
}
