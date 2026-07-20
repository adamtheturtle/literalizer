fn main() {
    fn make_widget<A>(_count: A) {}
    let my_data: serde_json::Value = serde_json::json!(make_widget(serde_json::json!(42)));
    let _ = my_data;
}
