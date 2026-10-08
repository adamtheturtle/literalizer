use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("minimum", -2147483648),
        ("below", -3000000000i64),
    ]);
    let _ = my_data;
}
