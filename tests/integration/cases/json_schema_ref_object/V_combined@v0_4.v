
fn main() {
	mut my_data := {
		'schema': {'\$ref': '#/defs/Foo'},
	}
	my_data = {
		'schema': {'\$ref': '#/defs/Foo'},
	}
	_ = my_data
}
