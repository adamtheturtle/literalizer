use std::collections::HashMap;
fn main() {
    struct ApiType;
    impl ApiType { fn fetch<A>(&self, _data: A) {} }
    struct ProcessType { api: ApiType }
    let process = ProcessType { api: ApiType };
    process.api.fetch(HashMap::from([("data", "hello")]));
    process.api.fetch(HashMap::from([("data", 42)]));
    process.api.fetch(HashMap::from([("data", true)]));
}
