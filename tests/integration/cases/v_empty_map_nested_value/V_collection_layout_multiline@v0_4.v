interface IVal {}

fn main() {
	my_data := [
		[
			{
				'mapping': map[string]IVal{},
			},
			map[string]map[string]IVal{},
		],
		[
			map[string]map[string]IVal{},
			{
				'mapping': map[string]IVal{},
			},
		],
	]
	_ = my_data
}
