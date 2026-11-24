use std::sync::LazyLock;
fn main() {
    static MY_DATA: LazyLock<f64> = LazyLock::new(|| 3.14);
    let _ = &MY_DATA;
}
