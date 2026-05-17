void main() {
int process(T...)(T args) { return 0; }
auto my_int = 1;
auto my_bool = true;
auto my_float = 3.14;
auto my_list = [
    1,
    2,
    3,
];
process(my_int, 42);
process(my_bool, 7);
process(my_float, 9);
process(my_list, 1);
}
