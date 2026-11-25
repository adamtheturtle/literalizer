#[derive(Clone)]
pub struct Record0 {
    pub labels: [&'static str; 1],
}
fn main() {
    let first = Record0 {
        labels: [
            "owned",
        ],
    };
    let my_data = first;
    let _ = &my_data;
}
