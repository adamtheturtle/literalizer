struct Record1 { long[] items; }
struct Record0 { Record1 outer; }
void main() {
auto record_data = Record1(
    [
        1,
        2,
    ],
);
auto my_data = Record0(
    record_data,
);
}
