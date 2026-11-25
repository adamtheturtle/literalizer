struct Record1 {
	x int
}
struct Record0 {
	values map[string]map[string]Record1
	flag bool
}

fn main() {
	my_data := Record0{
		values: {
			'outer': {
				'inner': Record1{
					x: 1,
				},
			},
		},
		flag: true,
	}
	_ = my_data
}
