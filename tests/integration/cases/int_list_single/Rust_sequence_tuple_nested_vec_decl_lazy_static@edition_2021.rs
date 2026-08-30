use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<Vec<i32>> = LazyLock::new(|| vec![
        1,
    ]);
    let _ = my_data;
}
