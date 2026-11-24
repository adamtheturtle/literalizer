struct Record1 { long count; long rate; }
struct Record2 { long retries; long timeout; }
struct Record0 { Record1 metrics; Record2 flags; }
void main() {
auto my_data = Record0(
    Record1(
        100,
        50,
    ),
    Record2(
        3,
        30,
    ),
);
}
