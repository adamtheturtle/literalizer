struct Record1 { long[] values; }
struct Record2 { long[][] nested; }
struct Record0 { Record1 trivial; Record2 nested; }
void main() {
auto trivial = Record1(
    [
        1,
        2,
    ],
);
auto nested = Record2(
    [
        [
            1,
            2,
        ],
        [
            3,
            4,
        ],
    ],
);
auto my_data = Record0(
    trivial,
    nested,
);
}
