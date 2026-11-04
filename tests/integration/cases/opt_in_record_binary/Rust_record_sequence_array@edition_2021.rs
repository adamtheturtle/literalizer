#[derive(Clone)]
pub struct Record0 {
    pub payload: &'static str,
}
fn main() {
    let my_data = Record0 {
        payload: "616263",
    };
    let _ = &my_data;
}
