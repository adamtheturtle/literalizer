use std::sync::LazyLock;
fn main() {
    static MY_DATA: LazyLock<Option<()>> = LazyLock::new(|| None::<()>);
    let _ = &MY_DATA;
}
