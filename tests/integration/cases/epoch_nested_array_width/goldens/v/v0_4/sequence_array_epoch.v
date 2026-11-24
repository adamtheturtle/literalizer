
fn main() {
	my_data := {
		'positive': [{'item': [i64(2147483648)]}],
		'negative': [{'item': [i64(-2147483649)]}],
		'mixed': [{'item': [i64(0), i64(2147483648)]}],
	}
	_ = my_data
}
