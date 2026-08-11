use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("schema", HashMap::from([("$ref", "#/defs/Foo")])),
    ]);
    my_data = HashMap::from([
        ("schema", HashMap::from([("$ref", "#/defs/Foo")])),
    ]);
    let _ = my_data;
}
