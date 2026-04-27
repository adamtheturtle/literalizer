interface IVal {}

fn main() {
	my_data := {
		'name': IVal('Alice'),
		'age': IVal(30),
		'active': IVal(true),
		'score': IVal(unsafe { nil }),
		'joined': IVal("2024-01-15"),
		'last_login': IVal("2024-01-15T12:30:00+00:00"),
		'avatar': IVal("48656c6c6f"),
	}
	_ = my_data
}
