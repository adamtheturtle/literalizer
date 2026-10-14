use std::sync::LazyLock;
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<Vec<String>> = LazyLock::new(|| Vec::<String>::new());
    let _ = &my_data;
}
