
fn main() {
	deep := {
		'_': '_',
	}
	my_data := {
		'a': {'b': {'c': deep.clone()}},
	}
	_ = my_data
}
