pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let value = GStr("12:30:15+02:00")
  let my_data = GDict([
    #("x", value),
  ])
  let _ = my_data
}
