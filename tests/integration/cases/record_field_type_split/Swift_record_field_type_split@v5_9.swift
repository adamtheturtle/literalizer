struct Record1 { let status: Int }
struct Record2 { let status: String }
struct Record4 { let kind: String; let urgent: Bool }
struct Record3 { let inner: Record4 }
struct Record6 { let error: String }
struct Record5 { let inner: Record6 }
struct Record7 { let holder: Record1 }
struct Record8 { let holder: Record2 }
struct Record9 { let nums: [Int] }
struct Record0 { let plain: Record1; let other: Record2; let nested_a: Record3; let nested_b: Record5; let wrap_a: Record7; let wrap_b: Record8; let wide: Record9 }
let my_data: Any = Record0(
    plain: Record1(
        status: 1,
    ),
    other: Record2(
        status: "ready",
    ),
    nested_a: Record3(
        inner: Record4(
            kind: "add",
            urgent: true,
        ),
    ),
    nested_b: Record5(
        inner: Record6(
            error: "not_found",
        ),
    ),
    wrap_a: Record7(
        holder: Record1(
            status: 2,
        ),
    ),
    wrap_b: Record8(
        holder: Record2(
            status: "word",
        ),
    ),
    wide: Record9(
        nums: [
            1,
            1099511627776,
        ],
    ),
)
