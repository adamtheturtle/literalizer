interface IVal {}

fn main() {
	empty_values := []int{}
	integer_values := [
		1,
	]
	my_data := [
		empty_values.clone(),
		integer_values.clone(),
	]
	_ = my_data
}
