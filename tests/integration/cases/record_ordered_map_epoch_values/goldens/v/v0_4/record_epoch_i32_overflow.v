struct Record0 {
	values map[string]i64
	flag bool
	nested_values map[string]map[string]i64
	list_values map[string][]i64
}

fn main() {
	my_data := Record0{
		values: {
			'first': i64(2208988800),
		},
		flag: true,
		nested_values: {
			'first': {
				'nested': i64(2208988800),
			},
		},
		list_values: {
			'first': [
				i64(2208988800),
			],
		},
	}
	_ = my_data
}
