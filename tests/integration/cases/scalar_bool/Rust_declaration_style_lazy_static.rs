use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<bool> = LazyLock::new(|| true);
    let _ = my_data;
}
