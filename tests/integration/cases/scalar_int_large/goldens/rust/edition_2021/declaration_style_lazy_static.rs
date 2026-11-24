use std::sync::LazyLock;
fn main() {
    static MY_DATA: LazyLock<i64> = LazyLock::new(|| 2147483648i64);
    let _ = &MY_DATA;
}
