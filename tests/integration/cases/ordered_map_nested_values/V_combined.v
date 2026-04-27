interface IVal {}

fn main() {
	mut my_data := {
		'name': IVal('Alice'),
		'scores': IVal({'1': 'first', '2': 'second'}),
	}
	my_data = {
		'name': IVal('Alice'),
		'scores': IVal({'1': 'first', '2': 'second'}),
	}
	_ = my_data
}
