void main() {
int process(T...)(T args) { return 0; }
auto arena = [
    "a": 1,
];
auto ZVal = [
    "a": 1,
];
auto ZKV = [
    "a": 1,
];
process(arena);
process(ZVal);
process(ZKV);
}
