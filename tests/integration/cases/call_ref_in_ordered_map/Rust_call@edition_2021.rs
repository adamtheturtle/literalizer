use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    fn process<A>(_a: A) {}
    let big_list = vec![
        "x",
    ];
    process(HashMap::from([("m", big_list)]));
}
