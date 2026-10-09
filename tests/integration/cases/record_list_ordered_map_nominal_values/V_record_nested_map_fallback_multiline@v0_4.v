struct Record1 {
	x int
}
struct Record0 {
	values []map[string]Record1
	flag bool
}

fn main() {
	my_data := Record0{
		values: [
			{
				'inner': Record1{
					x: 1,
				},
			},
			{
				'inner': Record1{
					x: 2,
				},
			},
		],
		flag: true,
	}
	_ = my_data
}
