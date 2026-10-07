pub type GVal0 {
  GVal0(birthday: String, moment: String, at: String)
}

pub fn main() {
  let my_data = GVal0(
    birthday: "2024-01-15",
    moment: "2024-01-15T12:30:00+00:00",
    at: "09:30:00",
  )
  let _ = my_data
}
