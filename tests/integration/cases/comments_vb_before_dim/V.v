interface IVal {}

fn main() {
	my_data := {
		// Configuration
		'name': IVal('app'),
		// Port setting
		'port': IVal(3000),
	}
	_ = my_data
}
