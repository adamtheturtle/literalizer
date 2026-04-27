interface IVal {}

fn main() {
	my_data := {
		'host': IVal('localhost'),
		'port': IVal(unsafe { nil }),  // not configured yet
	}
	_ = my_data
}
