struct Record0 { string name; long[] values; }
void main() {
int consume(T...)(T args) { return 0; }
auto item = Record0(
    "first",
    [
        1,
        2,
    ],
);
consume(item);
}
