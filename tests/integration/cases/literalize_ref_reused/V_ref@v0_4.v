
fn main() {
	shared_var := {
		'_': '_',
	}
	my_data := [
		shared_var.clone(),
		shared_var.clone(),
	]
	_ = my_data
}
