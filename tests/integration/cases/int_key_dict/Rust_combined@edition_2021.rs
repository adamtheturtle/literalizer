use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        (1, "one"),
        (2, "two"),
        (42, "answer"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        (1, "one"),
        (2, "two"),
        (42, "answer"),
    ]);
    let _ = &mut my_data;
}
