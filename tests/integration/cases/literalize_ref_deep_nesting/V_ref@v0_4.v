
fn main() {
	deep := [
		[
			1,
			2,
		],
		[
			3,
			4,
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
