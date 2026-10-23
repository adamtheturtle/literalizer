#+feature dynamic-literals
package main

main :: proc() {
value: any = nil
my_data := value
_ = my_data
}
