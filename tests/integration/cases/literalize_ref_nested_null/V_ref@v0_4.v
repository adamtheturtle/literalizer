
fn main() {
	my_null := unsafe { nil }
	my_data := [
		my_null.clone(),
		unsafe { nil },
	]
	_ = my_data
}
