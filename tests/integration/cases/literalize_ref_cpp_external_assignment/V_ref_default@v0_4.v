
fn main() {
	ref_data := [
		1,
		2,
	]
	my_data := [
		0,
	]
	(void)my_data;
	my_data = ref_data.clone()
	(void)my_data;
}
