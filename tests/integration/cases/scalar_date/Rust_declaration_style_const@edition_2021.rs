use chrono::NaiveDate;
fn main() {
    #[allow(non_upper_case_globals)]
    const my_data: NaiveDate = NaiveDate::from_ymd_opt(2024, 1, 15).unwrap();
    let _ = &my_data;
}
