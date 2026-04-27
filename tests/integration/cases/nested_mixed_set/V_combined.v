interface IVal {}

fn main() {
	mut my_data := {
		'name': IVal('Alice'),
		'tags': IVal([IVal(true), IVal(42), IVal('apple')]),
	}
	my_data = {
		'name': IVal('Alice'),
		'tags': IVal([IVal(true), IVal(42), IVal('apple')]),
	}
	_ = my_data
}
