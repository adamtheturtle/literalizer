use std::sync::LazyLock;
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<Option<()>> = LazyLock::new(|| None::<()>);
    let _ = &my_data;
}
