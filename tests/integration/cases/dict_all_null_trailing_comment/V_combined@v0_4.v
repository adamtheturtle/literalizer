
fn main() {
	mut my_data := {
		'a': unsafe { nil },
		'b': unsafe { nil },
		// trailing
	}
	my_data = {
		'a': unsafe { nil },
		'b': unsafe { nil },
		// trailing
	}
	_ = my_data
}
