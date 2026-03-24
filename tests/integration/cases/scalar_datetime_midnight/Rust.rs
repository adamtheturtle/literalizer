use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
fn main() {
    let my_data = NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(0, 0, 0).unwrap());
    let _ = my_data;
}
