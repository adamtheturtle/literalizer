
fn main() {
	my_null := unsafe { nil }
	my_data := [
		my_null,
		unsafe { nil },
	]
	_ = my_data
}
