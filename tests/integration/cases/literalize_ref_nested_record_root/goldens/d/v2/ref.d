struct Record1 { long value; }
struct Record0 { Record1 child; }
void main() {
auto first = Record0(
    Record1(
        1,
    ),
);
auto my_data = first;
}
