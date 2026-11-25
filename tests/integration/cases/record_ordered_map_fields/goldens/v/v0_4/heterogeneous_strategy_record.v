interface IVal {}
struct Record0 {
	numbers map[string]int
	words map[string]string
	nested map[string][]int
	empty map[string]IVal
	flag bool
	nested_maps map[string]map[string]int
	empty_nested_maps map[string]map[string]IVal
}

fn main() {
	my_data := Record0{
		numbers: {
			'first': 1,
		},
		words: {
			'first': 's',
		},
		nested: {
			'first': [
				1,
				2,
			],
		},
		empty: map[string]IVal{},
		flag: true,
		nested_maps: {
			'first': {
				'nested': 1,
			},
		},
		empty_nested_maps: {
			'first': map[string]IVal{},
		},
	}
	_ = my_data
}
