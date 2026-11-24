pub type GVal0 {
  GVal0(birthday: String, meeting: String, event_time: String)
}

pub fn main() {
  let my_data = GVal0(
    birthday: "2024-01-15",
    meeting: "09:30:00",
    event_time: "2024-01-15T12:30:00+00:00",
  )
  let _ = my_data
}
