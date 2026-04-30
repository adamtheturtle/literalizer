interface IVal {}

fn main() {
	mut my_data := [
		IVal({'\$ref': 'ref_x'}),
		IVal(1),
		IVal(2),
	]
	my_data = [
		IVal({'\$ref': 'ref_x'}),
		IVal(1),
		IVal(2),
	]
	_ = my_data
}
