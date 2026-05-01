
fn main() {
 my_var := {
 	'_': '_',
 }
 item_var := {
 	'_': '_',
 }
	my_data := {
		'key': my_var.clone(),
		'items': [item_var.clone(), {'fallback': 'value'}],
	}
	_ = my_data
}
