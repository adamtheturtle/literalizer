use chrono::NaiveDate;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = NaiveDate::from_ymd_opt(2024, 1, 15).unwrap();
    let _ = &mut my_data;
}
