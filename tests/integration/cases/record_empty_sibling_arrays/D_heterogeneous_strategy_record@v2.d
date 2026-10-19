struct Record1 { long item; }
struct Record2 { typeof(null) item; }
struct Record0 { Record1[][] integers; Record2[][] nulls; Record1[][][] nested; Record1[][] reversed; }
void main() {
auto my_data = Record0(
    [
        [],
        [
            Record1(
                1,
            ),
        ],
    ],
    [
        [],
        [
            Record2(
                null,
            ),
        ],
    ],
    [
        [
            [],
            [
                Record1(
                    2,
                ),
            ],
        ],
        [
            [
                Record1(
                    3,
                ),
            ],
            [],
        ],
    ],
    [
        [
            Record1(
                4,
            ),
        ],
        [],
    ],
);
}
