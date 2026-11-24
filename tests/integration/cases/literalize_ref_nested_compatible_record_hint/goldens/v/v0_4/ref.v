struct Record1 {
	items []int
}
struct Record0 {
	outer Record1
}

fn main() {
	record_data := Record1{
		items: [
			1,
			2,
		],
	}
	my_data := Record0{
		outer: record_data,
	}
	_ = my_data
}
