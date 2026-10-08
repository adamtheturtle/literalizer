struct Record1 { string x; }
struct Record2 { long x; }
struct Record0 { Record1 direct; Record2 bound; }
void main() {
auto first = Record2(
    1,
);
auto my_data = Record0(
    Record1(
        "s",
    ),
    first,
);
}
