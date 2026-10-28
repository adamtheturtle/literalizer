struct Record1 {
	x int
	y voidptr
}
struct Record2 {
	x voidptr
	y voidptr
}
struct Record3 {
	x int
	y int
}
struct Record0 {
	nullable Record1
	null_fields Record2
	plain Record3
}

fn main() {
	nullable := Record1{
		x: 1,
		y: unsafe { nil },
	}
	null_fields := Record2{
		x: unsafe { nil },
		y: unsafe { nil },
	}
	plain := Record3{
		x: 1,
		y: 2,
	}
	my_data := Record0{
		nullable: nullable,
		null_fields: null_fields,
		plain: plain,
	}
	_ = my_data
}
