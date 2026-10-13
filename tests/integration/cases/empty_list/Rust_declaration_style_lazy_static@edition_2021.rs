use std::sync::LazyLock;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<Vec<String>> = LazyLock::new(|| Vec::<String>::new());
    let _ = &my_data;
}
