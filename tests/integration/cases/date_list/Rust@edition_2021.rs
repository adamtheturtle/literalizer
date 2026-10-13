use chrono::NaiveDate;
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(),
        NaiveDate::from_ymd_opt(2024, 2, 20).unwrap(),
    ];
    let _ = &my_data;
}
