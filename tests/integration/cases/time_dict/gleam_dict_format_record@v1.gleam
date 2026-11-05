pub type GVal0 {
  GVal0(morning: String, afternoon: String, evening: String)
}

pub fn main() {
  let my_data = GVal0(
    morning: "09:30:00",
    afternoon: "14:15:00",
    evening: "23:59:59",
  )
  let _ = my_data
}
