interface IVal {}

fn main() {
	my_data := {
		'a': [IVal(1), IVal([]IVal{})],
	}
	_ = my_data
}
