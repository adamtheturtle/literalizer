use chrono::NaiveDate;
fn main() {
    let my_data = NaiveDate::from_ymd_opt(2024, 1, 15).unwrap();
    let _ = my_data;
}
