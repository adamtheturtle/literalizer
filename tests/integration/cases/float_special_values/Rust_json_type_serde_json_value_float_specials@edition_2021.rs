fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        f64::INFINITY,
        f64::NEG_INFINITY,
        f64::NAN,
    ]);
    let _ = my_data;
}
