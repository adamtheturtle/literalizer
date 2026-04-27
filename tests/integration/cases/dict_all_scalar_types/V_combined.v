interface IVal {}

fn main() {
	mut my_data := {
		's': IVal('string'),
		'i': IVal(1),
		'f': IVal(1.5),
		'b': IVal(true),
		'n': IVal(unsafe { nil }),
		'd': IVal("2024-01-15"),
		'dt': IVal("2024-01-15T12:00:00"),
		'by': IVal("48656c6c6f"),
	}
	my_data = {
		's': IVal('string'),
		'i': IVal(1),
		'f': IVal(1.5),
		'b': IVal(true),
		'n': IVal(unsafe { nil }),
		'd': IVal("2024-01-15"),
		'dt': IVal("2024-01-15T12:00:00"),
		'by': IVal("48656c6c6f"),
	}
	_ = my_data
}
