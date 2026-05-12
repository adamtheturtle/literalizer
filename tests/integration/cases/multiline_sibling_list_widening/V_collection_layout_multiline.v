interface IVal {}

fn main() {
	my_data := {
		'omap_value': IVal({
			'first': 1,
		}),
		'sibling_lists': IVal({
			'numbers': [
				1,
				2,
			],
			'strings': [
				'x',
				'y',
			],
		}),
		'ref_marker_present': IVal([
			'\$keep',
			'z',
		]),
	}
	_ = my_data
}
