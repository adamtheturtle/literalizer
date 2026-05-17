struct Record1 { string name; long age; }
struct Record0 { long id; Record1 owner; }
void main() {
auto my_data = Record0(
    1,
    Record1(
        "Alice",
        30,
    ),
);
}
