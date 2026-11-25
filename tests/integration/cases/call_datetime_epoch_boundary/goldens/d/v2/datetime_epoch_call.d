import std.json;
void main() {
int consume(T...)(T args) { return 0; }
consume(-2147483649);
consume(2147483648);
}
