use std::sync::LazyLock;
use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<HashMap<i32, &str>> = LazyLock::new(|| HashMap::from([
        (1, "one"),
        (2, "two"),
        (42, "answer"),
    ]));
    let _ = &my_data;
}
