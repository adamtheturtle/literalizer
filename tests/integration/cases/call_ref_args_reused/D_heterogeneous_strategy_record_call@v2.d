void main() {
int process(T...)(T args) { return 0; }
auto single_var = [
    4,
    5,
    6,
];
auto repeated_var = 1;
process(repeated_var, 1);
process(single_var, 0);
process(repeated_var, 8);
}
