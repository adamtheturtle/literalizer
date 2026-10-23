struct Record1 { long x; typeof(null) y; }
struct Record2 { typeof(null) x; typeof(null) y; }
struct Record3 { long x; long y; }
struct Record0 { Record1 nullable; Record2 null_fields; Record3 plain; }
void main() {
auto nullable = Record1(
    1,
    null,
);
auto null_fields = Record2(
    null,
    null,
);
auto plain = Record3(
    1,
    2,
);
auto my_data = Record0(
    nullable,
    null_fields,
    plain,
);
}
