use std::collections::HashMap;
fn main() {
    let std = HashMap::from([
        ("nan", f64::NAN),
        ("positive", f64::INFINITY),
        ("negative", f64::NEG_INFINITY),
    ]);
    let _ = &std;
}
