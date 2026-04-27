interface IVal {}

fn main() {
	mut my_data := {
		'host': IVal('localhost'),
		'port': IVal(unsafe { nil }),  // not configured yet
	}
	my_data = {
		'host': IVal('localhost'),
		'port': IVal(unsafe { nil }),  // not configured yet
	}
	_ = my_data
}
