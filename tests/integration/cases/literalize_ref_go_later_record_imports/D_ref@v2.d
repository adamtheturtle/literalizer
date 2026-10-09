struct Record1 { long x; }
struct Record2 { string day; string stamp; }
struct Record0 { Record1 plain; Record2 timed; }
void main() {
auto plain = Record1(
    1,
);
auto timed = Record2(
    "2001-01-02",
    "2001-01-02T03:04:05+00:00",
);
auto my_data = Record0(
    plain,
    timed,
);
}
