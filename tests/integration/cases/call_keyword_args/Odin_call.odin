#+feature dynamic-literals
package main

main :: proc() {
print(throttler.check("user_1", 1000.0))
print(throttler.check("user_2", 2000.5))
_ = my_data
}
