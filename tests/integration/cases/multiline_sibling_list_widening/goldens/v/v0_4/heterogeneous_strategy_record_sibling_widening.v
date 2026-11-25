struct Record1 {
	numbers []int
	strings []string
}
struct Record0 {
	omap_value map[string]int
	sibling_lists Record1
	ref_marker_present []string
}

fn main() {
	my_data := Record0{
		omap_value: {
			'first': 1,
		},
		sibling_lists: Record1{
			numbers: [
				1,
				2,
			],
			strings: [
				'x',
				'y',
			],
		},
		ref_marker_present: [
			'\$keep',
			'z',
		],
	}
	_ = my_data
}
