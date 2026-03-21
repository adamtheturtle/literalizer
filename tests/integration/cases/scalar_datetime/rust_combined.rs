use chrono::{NaiveDate, NaiveDateTime, NaiveTime};
fn main() {
    {
        let my_data = NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(12, 30, 0).unwrap());
        let _ = my_data;
    }
    let my_data;
    my_data = NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(12, 30, 0).unwrap());
    let _ = my_data;
}
