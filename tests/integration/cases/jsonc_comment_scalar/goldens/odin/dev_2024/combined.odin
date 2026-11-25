#+feature dynamic-literals
package main

main :: proc() {
// scalar heading
// second heading line
my_data := 42  // scalar inline
// inline continuation
// scalar trailing
// scalar heading
// second heading line
my_data = 42  // scalar inline
// inline continuation
// scalar trailing
_ = my_data
}
