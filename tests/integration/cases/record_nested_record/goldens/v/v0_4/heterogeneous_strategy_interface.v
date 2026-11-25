interface IVal {}

fn main() {
	my_data := {
		'id': IVal(1),
		'owner': IVal({'name': IVal('Alice'), 'age': IVal(30)}),
	}
	_ = my_data
}
