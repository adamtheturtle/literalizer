struct Record1 { long a; string b; typeof(null) c; }
struct Record0 { Record1 outer; }
void main() {
auto my_data = Record0(
    Record1(
        1,
        "x",
        null,
    ),
);
}
