use std::collections::BTreeMap;
fn main() {
    let my_data = BTreeMap::from([
        ("positive", f64::INFINITY),
        ("negative", f64::NEG_INFINITY),
        ("nan_value", f64::NAN),
    ]);
    let _ = my_data;
}
