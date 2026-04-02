use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
use std::collections::HashMap;
fn main() {
    {
        let mut my_data = HashMap::from([
            ("name", "Alice"),
            ("age", "30"),
            ("active", "True"),
            ("score", "None"),
            ("joined", "2024-01-15"),
            ("last_login", "2024-01-15T12:30:00+00:00"),
            ("avatar", "48656c6c6f"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("name", "Alice"),
        ("age", "30"),
        ("active", "True"),
        ("score", "None"),
        ("joined", "2024-01-15"),
        ("last_login", "2024-01-15T12:30:00+00:00"),
        ("avatar", "48656c6c6f"),
    ]);
    let _ = my_data;
}
