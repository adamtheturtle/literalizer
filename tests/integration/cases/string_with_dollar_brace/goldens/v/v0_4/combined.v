
fn main() {
	mut my_data := [
		'prefix \${HOME} suffix',
		'\${interpolated}',
	]
	my_data = [
		'prefix \${HOME} suffix',
		'\${interpolated}',
	]
	_ = my_data
}
