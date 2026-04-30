import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto shared = JSONValue(1);
auto other = JSONValue(2);
process(shared, 1);
process(other, 0);
process(shared, 8);
}
