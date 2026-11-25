// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn process<A>(_value: A) {}
    fn emit<A, B>(__call: A, __zip: B) {}
    emit(process(serde_json::json!(1)), serde_json::json!("2024-01-15T12:00:00"));
}
