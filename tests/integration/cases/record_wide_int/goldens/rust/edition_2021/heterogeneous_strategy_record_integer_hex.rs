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
        quantity: 0xf4240,
        big: 0xffffffffffffffffi128,
        ratio: 2.5,
        label: "tag",
        ok: true,
    };
    let _ = &my_data;
}
