use std::collections::{HashMap};
use chrono::{NaiveDate, NaiveDateTime, NaiveTime};
fn main() {
    let _ = HashMap::from([
        ("date", "2024-01-15"),
        ("datetime", "2024-01-15T12:30:00+00:00"),
    ]);
}
