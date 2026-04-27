interface IVal {}

fn main() {
	mut my_data := {
		// Server configuration
		'host': IVal('localhost'),  // default host
		'port': IVal(8080),
		// Enable debug mode
		'debug': IVal(true),
	}
	my_data = {
		// Server configuration
		'host': IVal('localhost'),  // default host
		'port': IVal(8080),
		// Enable debug mode
		'debug': IVal(true),
	}
	_ = my_data
}
