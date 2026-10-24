interface IVal {}
struct Record0 {
	bound IVal
}

fn main() {
	empty_map := map[string]IVal{}
	my_data := Record0{
		bound: empty_map.clone(),
	}
	_ = my_data
}
