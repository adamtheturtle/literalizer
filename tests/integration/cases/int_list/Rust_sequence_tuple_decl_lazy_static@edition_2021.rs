use std::sync::LazyLock;
fn main() {
    static MY_DATA: LazyLock<(i32, i32, i32)> = LazyLock::new(|| (
        1,
        2,
        3,
    ));
    let _ = &MY_DATA;
}
