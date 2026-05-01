use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("a", Vec::<String>::new()),
        ("b", Vec::<String>::new()),
    ]);
    my_data = HashMap::from([
        ("a", Vec::<String>::new()),
        ("b", Vec::<String>::new()),
    ]);
    let _ = my_data;
}
