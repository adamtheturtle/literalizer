struct Record1 {
	name string
	age int
}
struct Record0 {
	id int
	owner Record1
}

fn main() {
	my_data := Record0{
		id: 1,
		owner: Record1{
			name: 'Alice',
			age: 30,
		},
	}
	_ = my_data
}
