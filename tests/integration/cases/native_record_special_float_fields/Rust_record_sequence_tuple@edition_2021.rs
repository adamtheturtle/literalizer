#[derive(Clone)]
pub struct Record0 {
    pub positive: f64,
    pub negative: f64,
    pub nan_value: f64,
    pub finite: f64,
}
fn main() {
    let my_data = Record0 {
        positive: f64::INFINITY,
        negative: f64::NEG_INFINITY,
        nan_value: f64::NAN,
        finite: 1.5,
    };
    let _ = &my_data;
}
