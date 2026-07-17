use std::sync::LazyLock;
use std::collections::HashMap;
fn main() {
    static my_data: LazyLock<HashMap<&str, i64>> = LazyLock::new(|| HashMap::from([
        ("a", 1),
        ("b", 1099511627776i64),
    ]));
    let _ = my_data;
}
