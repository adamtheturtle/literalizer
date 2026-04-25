use chrono::NaiveDate;
fn main() {
    let mut my_data = vec![
        vec![NaiveDate::from_ymd_opt(2026, 1, 1).unwrap(), NaiveDate::from_ymd_opt(2026, 1, 2).unwrap()],
        vec![],
        vec![NaiveDate::from_ymd_opt(2026, 2, 3).unwrap(), NaiveDate::from_ymd_opt(2026, 2, 4).unwrap()],
    ];
    my_data = vec![
        vec![NaiveDate::from_ymd_opt(2026, 1, 1).unwrap(), NaiveDate::from_ymd_opt(2026, 1, 2).unwrap()],
        vec![],
        vec![NaiveDate::from_ymd_opt(2026, 2, 3).unwrap(), NaiveDate::from_ymd_opt(2026, 2, 4).unwrap()],
    ];
    let _ = my_data;
}
