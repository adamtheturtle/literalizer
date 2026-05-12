interface IVal {}

fn main() {
	my_data := {
		'sibling_lists': IVal({'numbers': [1, 2], 'strings': ['x', 'y']}),
		'ref_marker_present': IVal(['\$keep', 'z']),
	}
	_ = my_data
}
