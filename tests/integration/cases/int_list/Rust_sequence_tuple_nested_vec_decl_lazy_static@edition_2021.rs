use std::sync::LazyLock;
fn main() {
    static MY_DATA: LazyLock<Vec<i32>> = LazyLock::new(|| vec![
        1,
        2,
        3,
    ]);
    let _ = &MY_DATA;
}
