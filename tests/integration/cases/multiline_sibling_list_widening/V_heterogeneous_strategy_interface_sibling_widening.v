interface IVal {}

fn main() {
	my_data := {
		'omap_value': IVal({'first': 1}),
		'sibling_lists': IVal({'numbers': [IVal(1), IVal(2)], 'strings': [IVal('x'), IVal('y')]}),
		'ref_marker_present': IVal(['\$keep', 'z']),
	}
	_ = my_data
}
