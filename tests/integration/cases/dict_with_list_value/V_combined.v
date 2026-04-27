interface IVal {}

fn main() {
	mut my_data := {
		'name': IVal('Alice'),
		'scores': IVal([10, 20, 30]),
	}
	my_data = {
		'name': IVal('Alice'),
		'scores': IVal([10, 20, 30]),
	}
	_ = my_data
}
