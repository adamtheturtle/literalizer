use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<Vec<i64>> = LazyLock::new(|| vec![
        1,
        1099511627776i64,
    ]);
    let _ = my_data;
}
