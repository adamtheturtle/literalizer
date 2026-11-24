interface IVal {}

fn main() {
	my_data := [
		{'outer': {'inner': {'x': 1}}},
		{'outer': {'inner': map[string]int{}}},
	]
	_ = my_data
}
