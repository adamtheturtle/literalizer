pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("0a", GStr("first")),
    #("1b", GStr("second")),
  ])
  let _ = my_data
}
