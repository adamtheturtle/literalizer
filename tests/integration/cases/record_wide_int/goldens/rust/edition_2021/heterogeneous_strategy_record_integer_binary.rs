#[derive(Clone)]
pub struct Record0 {
    pub quantity: i32,
    pub big: i128,
    pub ratio: f64,
    pub label: &'static str,
    pub ok: bool,
}
fn main() {
    let my_data = Record0 {
        quantity: 0b11110100001001000000,
        big: 0b1111111111111111111111111111111111111111111111111111111111111111i128,
        ratio: 2.5,
        label: "tag",
        ok: true,
    };
    let _ = &my_data;
}
