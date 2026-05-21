fn main() {
    fn process<A>(_value: A) {}
    process(serde_json::json!("hello"));
    process(serde_json::json!(42));
    process(serde_json::json!(true));
}
