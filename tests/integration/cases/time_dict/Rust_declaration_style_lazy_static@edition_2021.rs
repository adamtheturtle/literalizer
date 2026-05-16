use std::sync::LazyLock;
use std::collections::HashMap;
fn main() {
    static my_data: LazyLock<HashMap<&str, &str>> = LazyLock::new(|| HashMap::from([
        ("morning", "09:30:00"),
        ("afternoon", "14:15:00"),
        ("evening", "23:59:59"),
    ]));
    let _ = my_data;
}
