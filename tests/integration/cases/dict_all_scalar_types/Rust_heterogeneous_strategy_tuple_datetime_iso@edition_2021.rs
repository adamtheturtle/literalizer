use chrono::NaiveDate;
#[derive(Clone)]
pub struct Record0 {
    pub s: &'static str,
    pub i: i32,
    pub f: f64,
    pub b: bool,
    pub n: Option<()>,
    pub d: NaiveDate,
    pub dt: &'static str,
    pub by: &'static str,
}
fn main() {
    let my_data = Record0 {
        s: "string",
        i: 1,
        f: 1.5,
        b: true,
        n: None::<()>,
        d: NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(),
        dt: "2024-01-15T12:00:00",
        by: "48656c6c6f",
    };
    let _ = &my_data;
}
