use std::sync::LazyLock;
use std::collections::BTreeMap;
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<BTreeMap<i32, &str>> = LazyLock::new(|| BTreeMap::from([
        (1, "one"),
        (2, "two"),
        (42, "answer"),
    ]));
    let _ = &my_data;
}
