use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("key", "it's here"),  // a comment
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("key", "it's here"),  // a comment
    ]);
    let _ = &mut my_data;
}
