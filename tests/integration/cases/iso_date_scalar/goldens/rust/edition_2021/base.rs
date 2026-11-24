use chrono::NaiveDate;
fn main() {
    let my_data = NaiveDate::from_ymd_opt(2000, 1, 1).unwrap();
    let _ = &my_data;
}
