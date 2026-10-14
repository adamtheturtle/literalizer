use std::collections::BTreeMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = BTreeMap::from([
        (1, "one"),
        (2, "two"),
        (42, "answer"),
    ]);
    let _ = &mut my_data;
}
