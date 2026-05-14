use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<Option<()>> = LazyLock::new(|| None::<()>);
    let _ = my_data;
}
