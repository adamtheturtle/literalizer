#+feature dynamic-literals
package main

main :: proc() {
// An anchor and an alias marker, written only inside this comment: &a *a
my_data: any = nil
_ = my_data
}
