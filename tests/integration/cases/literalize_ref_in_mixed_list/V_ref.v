interface IVal {}

fn main() {
 ref_x := {
 	'_': '_',
 }
	my_data := [
		IVal(ref_x.clone()),
		IVal(1),
		IVal(2),
	]
	_ = my_data
}
