use std::collections::HashMap;
fn main() {
    // empty heading
    // empty body
    // after empty
    let mut my_data = HashMap::<String, String>::from([]);
    let _ = &my_data;
    // empty heading
    // empty body
    // after empty
    my_data = HashMap::<String, String>::from([]);
    let _ = &mut my_data;
}
