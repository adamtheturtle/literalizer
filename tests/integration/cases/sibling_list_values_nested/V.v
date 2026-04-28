interface IVal {}

fn main() {
	my_data := {
		'lint': [IVal(2), IVal([]IVal{})],
		'test': [IVal(5), IVal(['compile'])],
	}
	_ = my_data
}
