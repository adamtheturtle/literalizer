use chrono::NaiveDate;
fn main() {
    static my_data: NaiveDate = NaiveDate::from_ymd_opt(2024, 1, 15).unwrap();
    let _ = my_data;
}
