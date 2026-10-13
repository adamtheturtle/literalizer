use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("a", Vec::<String>::new()),
        ("b", Vec::<String>::new()),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("a", Vec::<String>::new()),
        ("b", Vec::<String>::new()),
    ]);
    let _ = &mut my_data;
}
