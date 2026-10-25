use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
fn main() {
    let my_data = NaiveDateTime::new(NaiveDate::from_ymd_opt(2099, 6, 15).unwrap(), NaiveTime::from_hms_opt(8, 30, 0).unwrap());
    let _ = &my_data;
}
