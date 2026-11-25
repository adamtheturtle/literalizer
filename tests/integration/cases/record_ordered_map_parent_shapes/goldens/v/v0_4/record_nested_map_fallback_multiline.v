struct Record2 {
	x int
}
struct Record1 {
	values map[string]Record2
	flag bool
}
struct Record4 {
	y int
}
struct Record3 {
	values map[string]Record4
	flag bool
}
struct Record0 {
	first Record1
	second Record3
}

fn main() {
	my_data := Record0{
		first: Record1{
			values: {
				'item': Record2{
					x: 1,
				},
			},
			flag: true,
		},
		second: Record3{
			values: {
				'item': Record4{
					y: 2,
				},
			},
			flag: false,
		},
	}
	_ = my_data
}
