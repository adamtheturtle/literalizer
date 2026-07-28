use std::collections::HashMap;
fn main() {
    fn process<A>(_data: A) {}
    let my_list = Vec::<String>::new();
    process(vec![vec![HashMap::from([("inner", my_list)])]]);
}
