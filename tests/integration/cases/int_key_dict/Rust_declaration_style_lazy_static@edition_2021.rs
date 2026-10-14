use std::sync::LazyLock;
use std::collections::HashMap;
fn main() {
    static MY_DATA: LazyLock<HashMap<i32, &str>> = LazyLock::new(|| HashMap::from([
        (1, "one"),
        (2, "two"),
        (42, "answer"),
    ]));
    let _ = &MY_DATA;
}
