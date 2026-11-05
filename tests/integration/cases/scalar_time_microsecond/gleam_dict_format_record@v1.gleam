pub type GVal0 {
  GVal0(exact_millisecond: String, sub_millisecond: String)
}

pub fn main() {
  let my_data = GVal0(
    exact_millisecond: "09:30:15.123000",
    sub_millisecond: "09:30:15.123456",
  )
  let _ = my_data
}
