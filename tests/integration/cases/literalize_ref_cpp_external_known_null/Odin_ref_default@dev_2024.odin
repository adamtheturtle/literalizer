#+feature dynamic-literals
package main

main :: proc() {
item: any = nil
my_data: any = nil
(void)my_data;
my_data = item
(void)my_data;
}
