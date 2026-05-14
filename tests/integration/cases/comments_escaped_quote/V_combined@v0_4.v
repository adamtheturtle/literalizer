
fn main() {
	mut my_data := {
		'key': 'value " # not a comment',  // real
	}
	my_data = {
		'key': 'value " # not a comment',  // real
	}
	_ = my_data
}
