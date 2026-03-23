use chrono::NaiveDate;
fn main() {
    let _ = vec![
        NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(),
        NaiveDate::from_ymd_opt(2024, 2, 20).unwrap(),
    ];
}
