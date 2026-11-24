use std::sync::LazyLock;
use std::collections::HashMap;
fn main() {
    static MY_DATA: LazyLock<HashMap<String, String>> = LazyLock::new(|| HashMap::<String, String>::from([]));
    let _ = &MY_DATA;
}
