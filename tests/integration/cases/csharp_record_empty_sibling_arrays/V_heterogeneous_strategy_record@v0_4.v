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
			[]Record1{},
			[
				Record1{
					item: 1,
				},
			],
		],
		nulls: [
			[]Record2{},
			[
				Record2{
					item: unsafe { nil },
				},
			],
		],
		nested: [
			[
				[]Record1{},
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
				[]Record1{},
			],
		],
		reversed: [
			[
				Record1{
					item: 4,
				},
			],
			[]Record1{},
		],
	}
	_ = my_data
}
