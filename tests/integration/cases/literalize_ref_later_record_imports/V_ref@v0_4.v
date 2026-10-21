struct Record1 {
	x int
}
struct Record2 {
	day string
	stamp string
}
struct Record0 {
	plain Record1
	timed Record2
}

fn main() {
	plain := Record1{
		x: 1,
	}
	timed := Record2{
		day: "2001-01-02",
		stamp: "2001-01-02T03:04:05+00:00",
	}
	my_data := Record0{
		plain: plain,
		timed: timed,
	}
	_ = my_data
}
