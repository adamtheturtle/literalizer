struct Record1 {
	count int
	rate int
}
struct Record2 {
	retries int
	timeout int
}
struct Record0 {
	metrics Record1
	flags Record2
}

fn main() {
	my_data := Record0{
		metrics: Record1{
			count: 100,
			rate: 50,
		},
		flags: Record2{
			retries: 3,
			timeout: 30,
		},
	}
	_ = my_data
}
