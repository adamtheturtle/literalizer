pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("within_i32", GStr("2024-01-15T12:00:00")),
    #("beyond_i32", GStr("2099-06-15T08:30:00")),
  ])
  let my_data = GDict([
    #("within_i32", GStr("2024-01-15T12:00:00")),
    #("beyond_i32", GStr("2099-06-15T08:30:00")),
  ])
  let _ = my_data
}
