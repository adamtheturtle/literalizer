struct Record1 {
	x string
}
struct Record2 {
	x int
}
struct Record0 {
	direct Record1
	bound Record2
}

fn main() {
	first := Record2{
		x: 1,
	}
	my_data := Record0{
		direct: Record1{
			x: 's',
		},
		bound: first.clone(),
	}
	_ = my_data
}
