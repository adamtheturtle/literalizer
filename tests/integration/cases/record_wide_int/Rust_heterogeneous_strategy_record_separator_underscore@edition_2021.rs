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
        quantity: 1_000_000,
        big: 18_446_744_073_709_551_615i128,
        ratio: 2.5,
        label: "tag",
        ok: true,
    };
    let _ = &my_data;
}
