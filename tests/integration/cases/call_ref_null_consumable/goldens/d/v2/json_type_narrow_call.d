void main() {
int consume(T...)(T args) { return 0; }
auto my_null = null;
auto regular_null = null;
consume(my_null);
consume(regular_null);
}
