use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(12, 30, 0).unwrap());
    let _ = &my_data;
    my_data = NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(12, 30, 0).unwrap());
    let _ = &mut my_data;
}
