use std::sync::LazyLock;
use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<Vec<HashMap<&str, i32>>> = LazyLock::new(|| vec![
        HashMap::from([("a", 1)]),
        <HashMap<&str, i32>>::from([]),
    ]);
    let _ = &my_data;
}
