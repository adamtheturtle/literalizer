interface IVal {}
struct Record0 {
	name string
	payload map[string]IVal
}

fn main() {
	my_data := [
		Record0{
			name: 'one',
			payload: {
				'scalar': IVal(1),
				'items': IVal([]IVal{}),
			},
		},
		Record0{
			name: 'two',
			payload: {
				'other': IVal(2),
			},
		},
	]
	_ = my_data
}
