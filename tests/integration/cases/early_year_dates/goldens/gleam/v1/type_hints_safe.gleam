pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("date", GStr("0099-05-27")),
    #("naive", GStr("0001-01-01T12:30:00")),
    #("recent", GStr("2024-05-27T10:00:00")),
  ])
  let _ = my_data
}
