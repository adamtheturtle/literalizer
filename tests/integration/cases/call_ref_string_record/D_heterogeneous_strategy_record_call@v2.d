struct Record0 { string value; }
void main() {
int consume(T...)(T args) { return 0; }
auto item = Record0(
    "owned",
);
consume(item);
}
