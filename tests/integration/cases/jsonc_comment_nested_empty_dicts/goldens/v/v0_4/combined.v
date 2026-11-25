interface IVal {}

fn main() {
	mut my_data := {
		// outer heading
		// first empty
		'a': map[string]IVal{},
		// second empty
		'b': map[string]IVal{},
	}
	my_data = {
		// outer heading
		// first empty
		'a': map[string]IVal{},
		// second empty
		'b': map[string]IVal{},
	}
	_ = my_data
}
