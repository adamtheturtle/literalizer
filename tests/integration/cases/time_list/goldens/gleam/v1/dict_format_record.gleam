pub type GVal0 {
  GVal0(times: List(String))
}

pub fn main() {
  let my_data = GVal0(
    times: [
      "09:30:00",
      "17:45:00",
      "23:59:59",
    ],
  )
  let _ = my_data
}
