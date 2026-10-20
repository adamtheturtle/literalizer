struct Record1 {
	value int
}
struct Record0 {
	child Record1
}

fn main() {
	first := Record0{
		child: Record1{
			value: 1,
		},
	}
	my_data := first
	_ = my_data
}
