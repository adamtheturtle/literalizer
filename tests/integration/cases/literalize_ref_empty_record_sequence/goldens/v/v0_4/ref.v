interface IVal {}
struct Record0 {
	x int
}

fn main() {
	empty_items := []Record0{}
	populated_items := [
		Record0{ x: 1 },
	]
	my_data := [
		empty_items.clone(),
		populated_items.clone(),
	]
	_ = my_data
}
