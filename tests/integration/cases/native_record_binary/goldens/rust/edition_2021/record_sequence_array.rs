#[derive(Clone)]
pub struct Record0 {
    pub payload: &'static str,
}
fn main() {
    let my_data = Record0 {
        payload: "48656c6c6f",
    };
    let _ = &my_data;
}
