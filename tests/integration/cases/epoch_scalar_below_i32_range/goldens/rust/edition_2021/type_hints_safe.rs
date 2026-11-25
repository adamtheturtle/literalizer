use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
fn main() {
    let my_data = NaiveDateTime::new(NaiveDate::from_ymd_opt(1901, 12, 13).unwrap(), NaiveTime::from_hms_opt(20, 45, 51).unwrap());
    let _ = &my_data;
}
