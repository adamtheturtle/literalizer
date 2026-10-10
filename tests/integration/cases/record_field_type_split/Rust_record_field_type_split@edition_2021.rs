#[derive(Clone)]
struct Record1 {
    status: i32,
}
#[derive(Clone)]
struct Record2 {
    status: &'static str,
}
#[derive(Clone)]
struct Record4 {
    kind: &'static str,
    urgent: bool,
}
#[derive(Clone)]
struct Record3 {
    inner: Record4,
}
#[derive(Clone)]
struct Record6 {
    error: &'static str,
}
#[derive(Clone)]
struct Record5 {
    inner: Record6,
}
#[derive(Clone)]
struct Record7 {
    holder: Record1,
}
#[derive(Clone)]
struct Record8 {
    holder: Record2,
}
#[derive(Clone)]
struct Record9 {
    nums: Vec<i64>,
}
#[derive(Clone)]
struct Record0 {
    plain: Record1,
    other: Record2,
    nested_a: Record3,
    nested_b: Record5,
    wrap_a: Record7,
    wrap_b: Record8,
    wide: Record9,
}
fn main() {
    let my_data = Record0 {
        plain: Record1 {
            status: 1,
        },
        other: Record2 {
            status: "ready",
        },
        nested_a: Record3 {
            inner: Record4 {
                kind: "add",
                urgent: true,
            },
        },
        nested_b: Record5 {
            inner: Record6 {
                error: "not_found",
            },
        },
        wrap_a: Record7 {
            holder: Record1 {
                status: 2,
            },
        },
        wrap_b: Record8 {
            holder: Record2 {
                status: "word",
            },
        },
        wide: Record9 {
            nums: vec![
                1,
                1099511627776i64,
            ],
        },
    };
    let _ = my_data;
}
