use std::collections::HashMap;
fn main() {
    fn process<A>(_a: A) {}
    let big_list = vec![
        "x",
    ];
    process(HashMap::from([("m", big_list)]));
}
