interface IVal {}

fn main() {
	mut my_data := {
		'a': []IVal{},
		'b': []IVal{},
	}
	my_data = {
		'a': []IVal{},
		'b': []IVal{},
	}
	_ = my_data
}
