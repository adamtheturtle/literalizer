use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    fn process<A>(_data: A) {}
    let my_list = HashMap::from([
        ("unused", "value"),
    ]);
    process(vec![vec![HashMap::from([("inner", my_list)])]]);
}
