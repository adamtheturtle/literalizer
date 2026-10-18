
fn main() {
	my_data := {
		'i32_below': i64(-0x80000001),
		'i32_minimum': i64(-0x80000000),
		'i32_above': i64(-0x7fffffff),
		'i32_maximum': i64(0x7fffffff),
		'i32_over': i64(0x80000000),
		'i64_minimum': i64(-0x8000000000000000),
		'i64_maximum': i64(0x7fffffffffffffff),
	}
	_ = my_data
}
