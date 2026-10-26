use std::collections::HashMap;
fn main() {
    struct ApiType;
    impl ApiType { fn process<A>(&self, _self: A) {} }
    let api = ApiType;
    api.process(HashMap::<String, String>::from([]));
}
