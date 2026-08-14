
fn main() {
	deep := [
		[
			'one',
			'two',
		],
		[
			'three',
			'four',
		],
	]
	my_data := {
		'a': {
			'b': {
				'c': deep.clone(),
			},
		},
	}
	_ = my_data
}
