import math
struct Record0 {
	nan f64
	positive f64
	negative f64
}

fn main() {
	std := Record0{
		nan: math.nan(),
		positive: math.inf(1),
		negative: math.inf(-1),
	}
	_ = std
}
