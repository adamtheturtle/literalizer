use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        (true, "yes"),
        (false, "no"),
    ]);
    my_data = HashMap::from([
        (true, "yes"),
        (false, "no"),
    ]);
    let _ = my_data;
}
