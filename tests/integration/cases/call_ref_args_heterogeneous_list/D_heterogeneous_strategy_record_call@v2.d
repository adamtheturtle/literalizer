void main() {
int process(T...)(T args) { return 0; }
auto my_ints = [
    1,
    2,
    3,
];
auto my_strings = [
    "a",
    "b",
];
auto my_empty = [];
process(my_ints, 42);
process(my_strings, 7);
process(my_empty, 99);
}
