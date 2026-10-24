pub type GVal0 {
  GVal0(within_i32: String, beyond_i32: String)
}

pub fn main() {
  let my_data = GVal0(
    within_i32: "2024-01-15T12:00:00",
    beyond_i32: "2099-06-15T08:30:00",
  )
  let _ = my_data
}
