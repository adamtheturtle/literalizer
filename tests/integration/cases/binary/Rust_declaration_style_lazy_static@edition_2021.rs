use std::sync::LazyLock;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<Vec<&str>> = LazyLock::new(|| vec![
        "48656c6c6f",
    ]);
    let _ = &my_data;
}
