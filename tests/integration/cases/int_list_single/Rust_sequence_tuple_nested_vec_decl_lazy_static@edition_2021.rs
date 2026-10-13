use std::sync::LazyLock;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<Vec<i32>> = LazyLock::new(|| vec![
        1,
    ]);
    let _ = &my_data;
}
