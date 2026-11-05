use std::collections::HashMap;
fn main() {
    fn process<A, B>(_a: A, _b: B) {}
    let big_list = vec![
        "x",
    ];
    process(HashMap::from([("k", big_list)]), 2);
}
