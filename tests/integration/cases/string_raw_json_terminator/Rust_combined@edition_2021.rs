use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        (")json", "x"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        (")json", "x"),
    ]);
    let _ = &mut my_data;
}
