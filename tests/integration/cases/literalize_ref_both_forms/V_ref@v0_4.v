
fn main() {
	mut shared_values := [
		1,
		2,
	]
	mut my_data := {
		'a': shared_values.clone(),
	}
	my_data = {
		'a': shared_values.clone(),
	}
	_ = my_data
}
