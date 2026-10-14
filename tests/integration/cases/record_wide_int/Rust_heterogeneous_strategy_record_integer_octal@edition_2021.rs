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
        quantity: 0o3641100,
        big: 0o1777777777777777777777i128,
        ratio: 2.5,
        label: "tag",
        ok: true,
    };
    let _ = &my_data;
}
