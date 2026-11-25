import math

fn main() {
	std := {
		'nan': math.nan(),
		'positive': math.inf(1),
		'negative': math.inf(-1),
	}
	_ = std
}
