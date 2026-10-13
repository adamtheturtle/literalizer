use std::sync::LazyLock;
use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<HashMap<String, String>> = LazyLock::new(|| HashMap::<String, String>::from([]));
    let _ = &my_data;
}
