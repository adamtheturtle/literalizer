#[derive(Clone)]
pub struct Record1 {
    pub status: i32,
}
#[derive(Clone)]
pub struct Record2 {
    pub status: &'static str,
}
#[derive(Clone)]
pub struct Record4 {
    pub kind: &'static str,
    pub urgent: bool,
}
#[derive(Clone)]
pub struct Record3 {
    pub inner: Record4,
}
#[derive(Clone)]
pub struct Record6 {
    pub error: &'static str,
}
#[derive(Clone)]
pub struct Record5 {
    pub inner: Record6,
}
#[derive(Clone)]
pub struct Record7 {
    pub holder: Record1,
}
#[derive(Clone)]
pub struct Record8 {
    pub holder: Record2,
}
#[derive(Clone)]
pub struct Record9 {
    pub nums: Vec<i64>,
}
#[derive(Clone)]
pub struct Record0 {
    pub plain: Record1,
    pub other: Record2,
    pub nested_a: Record3,
    pub nested_b: Record5,
    pub wrap_a: Record7,
    pub wrap_b: Record8,
    pub wide: Record9,
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
    let _ = &my_data;
}
