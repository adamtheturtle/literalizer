#+feature dynamic-literals
package main
Record1 :: struct { status: int }
Record2 :: struct { status: string }
Record4 :: struct { kind: string, urgent: bool }
Record3 :: struct { inner: Record4 }
Record6 :: struct { error: string }
Record5 :: struct { inner: Record6 }
Record7 :: struct { holder: Record1 }
Record8 :: struct { holder: Record2 }
Record9 :: struct { nums: [dynamic]any }
Record0 :: struct { plain: Record1, other: Record2, nested_a: Record3, nested_b: Record5, wrap_a: Record7, wrap_b: Record8, wide: Record9 }

main :: proc() {
my_data := Record0{
	plain = Record1{
		status = 1,
	},
	other = Record2{
		status = "ready",
	},
	nested_a = Record3{
		inner = Record4{
			kind = "add",
			urgent = true,
		},
	},
	nested_b = Record5{
		inner = Record6{
			error = "not_found",
		},
	},
	wrap_a = Record7{
		holder = Record1{
			status = 2,
		},
	},
	wrap_b = Record8{
		holder = Record2{
			status = "word",
		},
	},
	wide = Record9{
		nums = [dynamic]any{
			1,
			1099511627776,
		},
	},
}
_ = my_data
}
