
fn main() {
	mut my_data := {
		'a': {'b': {'c': {'\$ref': 'deep'}}},
	}
	my_data = {
		'a': {'b': {'c': {'\$ref': 'deep'}}},
	}
	_ = my_data
}
