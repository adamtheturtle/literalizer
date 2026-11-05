pub type GVal {
  JStr(String)
  JDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = JDict([
    #("date", JStr("0099-05-27")),
    #("naive", JStr("0001-01-01T12:30:00")),
    #("recent", JStr("2024-05-27T10:00:00")),
  ])
  let _ = my_data
}
