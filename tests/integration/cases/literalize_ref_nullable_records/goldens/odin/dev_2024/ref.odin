#+feature dynamic-literals
package main
Record1 :: struct { x: int, y: any }
Record2 :: struct { x: any, y: any }
Record3 :: struct { x: int, y: int }
Record0 :: struct { nullable: Record1, null_fields: Record2, plain: Record3 }

main :: proc() {
nullable := Record1{
	x = 1,
	y = nil,
}
null_fields := Record2{
	x = nil,
	y = nil,
}
plain := Record3{
	x = 1,
	y = 2,
}
my_data := Record0{
	nullable = nullable,
	null_fields = null_fields,
	plain = plain,
}
_ = my_data
}
