use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("$ref", "myVar"),
    ]);
    my_data = HashMap::from([
        ("$ref", "myVar"),
    ]);
    let _ = my_data;
}
