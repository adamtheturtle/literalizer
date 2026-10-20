#+feature dynamic-literals
package main

main :: proc() {
source_value := "￾￿"
my_data := source_value
_ = my_data
}
