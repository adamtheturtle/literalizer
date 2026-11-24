use std::sync::LazyLock;
fn main() {
    static MY_DATA: LazyLock<Vec<i64>> = LazyLock::new(|| vec![
        1,
        1099511627776i64,
    ]);
    let _ = &MY_DATA;
}
