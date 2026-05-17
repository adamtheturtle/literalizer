#+feature dynamic-literals
package main
Record0 :: struct { name: string, age: int, active: bool, score: f64 }

main :: proc() {
my_data := Record0{
	name = "Alice",
	age = 30,
	active = true,
	score = 4.5,
}
_ = my_data
}
