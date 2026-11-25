struct Record1 { long id; string label; }
struct Record0 { string name; Record1[] items; }
void main() {
auto my_data = Record0(
    "box",
    [
        Record1(
            1,
            "first",
        ),
        Record1(
            2,
            "second",
        ),
    ],
);
}
