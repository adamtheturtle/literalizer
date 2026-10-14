use std::sync::LazyLock;
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<bool> = LazyLock::new(|| true);
    let _ = &my_data;
}
