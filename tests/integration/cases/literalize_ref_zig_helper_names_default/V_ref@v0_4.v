
fn main() {
	std := {
		'a': 1,
	}
	arena := {
		'a': 1,
	}
	allocator := {
		'a': 1,
	}
	my_data := [
		std.clone(),
		arena.clone(),
		allocator.clone(),
	]
	_ = my_data
}
