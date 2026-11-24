#[derive(Clone)]
pub struct Record0 {
    pub narrow_pair: (i32, i32),
    pub wide_pair: (i32, i64),
    pub wide_triple: (i32, i32, i64),
    pub beyond_pair: (i128, i128),
    pub beyond_triple: (i128, i128, i128),
    pub mixed_triple: (i32, &'static str, bool),
}
fn main() {
    let my_data = Record0 {
        narrow_pair: (
            1,
            2,
        ),
        wide_pair: (
            1,
            1099511627776i64,
        ),
        wide_triple: (
            1,
            2,
            1099511627776i64,
        ),
        beyond_pair: (
            1i128,
            18446744073709551616i128,
        ),
        beyond_triple: (
            1i128,
            2i128,
            18446744073709551616i128,
        ),
        mixed_triple: (
            1,
            "text",
            true,
        ),
    };
    let _ = &my_data;
}
