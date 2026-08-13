interface IVal {}
struct Record0 {
	f IVal
	g int
}

fn main() {
	my_data := Record0{
		f: map[string]IVal{},
		g: 1,
	}
	_ = my_data
}
