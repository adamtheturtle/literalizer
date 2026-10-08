struct Record1 {
	integer int
	boolean bool
	decimal f64
	null voidptr
}
struct Record3 {
	integer int
}
struct Record2 {
	child Record3
}
struct Record4 {
	text string
}
struct Record5 {
	day string
	stamp string
}
struct Record0 {
	trivial Record1
	nested Record2
	owning Record4
	calendar Record5
}

fn main() {
	trivial := Record1{
		integer: 1,
		boolean: true,
		decimal: 1.5,
		null: unsafe { nil },
	}
	nested := Record2{
		child: Record3{
			integer: 2,
		},
	}
	owning := Record4{
		text: 'owned',
	}
	calendar := Record5{
		day: "2001-01-02",
		stamp: "2001-01-02T03:04:05+00:00",
	}
	my_data := Record0{
		trivial: trivial,
		nested: nested,
		owning: owning,
		calendar: calendar,
	}
	_ = my_data
}
