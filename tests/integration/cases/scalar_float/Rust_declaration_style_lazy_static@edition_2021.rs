use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<f64> = LazyLock::new(|| 3.14);
    let _ = my_data;
}
