interface IVal {}

fn main() {
	my_data := {
		'name': IVal('Alice'),
		'scores': IVal([10, 20, 30]),
	}
	_ = my_data
}
