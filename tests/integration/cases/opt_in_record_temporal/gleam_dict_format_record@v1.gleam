pub type GVal0 {
  GVal0(event_date: String, event_time: String, event_datetime: String)
}

pub fn main() {
  let my_data = GVal0(
    event_date: "2024-01-15",
    event_time: "12:30:00",
    event_datetime: "2024-01-15T12:30:00+00:00",
  )
  let _ = my_data
}
