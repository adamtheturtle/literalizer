#+feature dynamic-literals
package main
Record1 :: struct { name: string, age: int }
Record0 :: struct { id: int, owner: Record1 }

main :: proc() {
my_data := Record0{
	id = 1,
	owner = Record1{
		name = "Alice",
		age = 30,
	},
}
_ = my_data
}
