#[derive(Clone)]
pub struct Record0 {
    pub nan: f64,
    pub positive: f64,
    pub negative: f64,
}
fn main() {
    let std = Record0 {
        nan: f64::NAN,
        positive: f64::INFINITY,
        negative: f64::NEG_INFINITY,
    };
    let _ = &std;
}
