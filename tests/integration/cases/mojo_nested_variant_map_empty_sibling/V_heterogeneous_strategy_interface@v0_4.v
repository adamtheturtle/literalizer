interface IVal {}

fn main() {
	my_data := [
		IVal({'nested': {'count': IVal(1), 'name': IVal('value')}}),
		IVal(map[string]IVal{}),
	]
	_ = my_data
}
