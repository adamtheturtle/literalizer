use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: NaiveDateTime = NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(12, 30, 0).unwrap());
    let _ = &my_data;
}
