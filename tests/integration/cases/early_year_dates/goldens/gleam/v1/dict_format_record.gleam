pub type GVal0 {
  GVal0(date: String, naive: String, recent: String)
}

pub fn main() {
  let my_data = GVal0(
    date: "0099-05-27",
    naive: "0001-01-01T12:30:00",
    recent: "2024-05-27T10:00:00",
  )
  let _ = my_data
}
