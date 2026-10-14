use std::sync::LazyLock;
use std::collections::BTreeMap;
fn main() {
    static MY_DATA: LazyLock<BTreeMap<i32, &str>> = LazyLock::new(|| BTreeMap::from([
        (1, "one"),
        (2, "two"),
        (42, "answer"),
    ]));
    let _ = &MY_DATA;
}
