struct Record1 { long status; }
struct Record2 { string status; }
struct Record4 { string kind; bool urgent; }
struct Record3 { Record4 inner; }
struct Record6 { string error; }
struct Record5 { Record6 inner; }
struct Record7 { Record1 holder; }
struct Record8 { Record2 holder; }
struct Record9 { long[] nums; }
struct Record0 { Record1 plain; Record2 other; Record3 nested_a; Record5 nested_b; Record7 wrap_a; Record8 wrap_b; Record9 wide; }
void main() {
auto my_data = Record0(
    Record1(
        1,
    ),
    Record2(
        "ready",
    ),
    Record3(
        Record4(
            "add",
            true,
        ),
    ),
    Record5(
        Record6(
            "not_found",
        ),
    ),
    Record7(
        Record1(
            2,
        ),
    ),
    Record8(
        Record2(
            "word",
        ),
    ),
    Record9(
        [
            1,
            1099511627776,
        ],
    ),
);
}
