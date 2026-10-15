interface IVal {}
struct Record1 {
	item int
}
struct Record2 {
	item voidptr
}
struct Record0 {
	integers [][]Record1
	nulls [][]Record2
	nested [][][]Record1
	reversed [][]Record1
}

fn main() {
	my_data := Record0{
		integers: [
			[]IVal{},
			[
				Record1{
					item: 1,
				},
			],
		],
		nulls: [
			[]IVal{},
			[
				Record2{
					item: unsafe { nil },
				},
			],
		],
		nested: [
			[
				[]IVal{},
				[
					Record1{
						item: 2,
					},
				],
			],
			[
				[
					Record1{
						item: 3,
					},
				],
				[]IVal{},
			],
		],
		reversed: [
			[
				Record1{
					item: 4,
				},
			],
			[]IVal{},
		],
	}
	_ = my_data
}
