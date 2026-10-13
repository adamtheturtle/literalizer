use std::sync::LazyLock;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<Vec<i64>> = LazyLock::new(|| vec![
        1,
        1099511627776i64,
    ]);
    let _ = &my_data;
}
