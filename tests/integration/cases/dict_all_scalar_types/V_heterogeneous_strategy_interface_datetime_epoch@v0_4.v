interface IVal {}

fn main() {
	my_data := {
		's': IVal('string'),
		'i': IVal(1),
		'f': IVal(1.5),
		'b': IVal(true),
		'n': IVal(unsafe { nil }),
		'd': IVal("2024-01-15"),
		'dt': IVal(1705320000),
		'by': IVal("48656c6c6f"),
	}
	_ = my_data
}
