struct Record1 {
	status int
}
struct Record2 {
	status string
}
struct Record4 {
	kind string
	urgent bool
}
struct Record3 {
	inner Record4
}
struct Record6 {
	error string
}
struct Record5 {
	inner Record6
}
struct Record7 {
	holder Record1
}
struct Record8 {
	holder Record2
}
struct Record9 {
	nums []i64
}
struct Record0 {
	plain Record1
	other Record2
	nested_a Record3
	nested_b Record5
	wrap_a Record7
	wrap_b Record8
	wide Record9
}

fn main() {
	my_data := Record0{
		plain: Record1{
			status: 1,
		},
		other: Record2{
			status: 'ready',
		},
		nested_a: Record3{
			inner: Record4{
				kind: 'add',
				urgent: true,
			},
		},
		nested_b: Record5{
			inner: Record6{
				error: 'not_found',
			},
		},
		wrap_a: Record7{
			holder: Record1{
				status: 2,
			},
		},
		wrap_b: Record8{
			holder: Record2{
				status: 'word',
			},
		},
		wide: Record9{
			nums: [
				i64(1),
				i64(1099511627776),
			],
		},
	}
	_ = my_data
}
