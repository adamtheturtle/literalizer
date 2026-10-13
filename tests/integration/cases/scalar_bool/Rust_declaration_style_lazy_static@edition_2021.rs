use std::sync::LazyLock;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<bool> = LazyLock::new(|| true);
    let _ = &my_data;
}
