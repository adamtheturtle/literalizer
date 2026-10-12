#[derive(Clone)]
struct Record0 {
    nan: f64,
    positive: f64,
    negative: f64,
}
fn main() {
    let std = Record0 {
        nan: f64::NAN,
        positive: f64::INFINITY,
        negative: f64::NEG_INFINITY,
    };
    let _ = std;
}
