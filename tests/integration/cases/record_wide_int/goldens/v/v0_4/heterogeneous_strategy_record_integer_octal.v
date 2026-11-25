struct Record0 {
	quantity int
	big u64
	ratio f64
	label string
	ok bool
}

fn main() {
	my_data := Record0{
		quantity: 0o3641100,
		big: u64(18446744073709551615),
		ratio: 2.5,
		label: 'tag',
		ok: true,
	}
	_ = my_data
}
