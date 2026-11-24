use chrono::NaiveDate;
fn main() {
    const MY_DATA: NaiveDate = NaiveDate::from_ymd_opt(2024, 1, 15).unwrap();
    let _ = &MY_DATA;
}
