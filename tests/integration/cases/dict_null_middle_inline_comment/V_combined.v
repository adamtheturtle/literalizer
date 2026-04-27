interface IVal {}

fn main() {
	mut my_data := {
		'host': IVal('localhost'),
		'port': IVal(unsafe { nil }),  // not configured yet
		'debug': IVal(true),
	}
	my_data = {
		'host': IVal('localhost'),
		'port': IVal(unsafe { nil }),  // not configured yet
		'debug': IVal(true),
	}
	_ = my_data
}
