use std::collections::HashMap;
fn main() {
    struct ProcessType;
    impl ProcessType { fn fetch<A>(&self, _data: A) {} }
    struct AppType { process: ProcessType }
    let app = AppType { process: ProcessType };
    app.process.fetch(HashMap::from([("data", "hello")]));
    app.process.fetch(HashMap::from([("data", 42)]));
    app.process.fetch(HashMap::from([("data", true)]));
}
