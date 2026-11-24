interface IVal {}

fn main() {
	my_data := [
		[IVal(1), IVal([]int{})],
		[IVal(2), IVal([3])],
	]
	_ = my_data
}
