use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("minimum", -2_147_483_648),
        ("below", -3_000_000_000i64),
    ]);
    let _ = &my_data;
}
