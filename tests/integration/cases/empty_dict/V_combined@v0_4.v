interface IVal {}

fn main() {
	mut my_data := map[string]IVal{}
	my_data = map[string]IVal{}
	_ = my_data
}
