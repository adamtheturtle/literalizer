pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("", GStr("unnamed")),
    #("named", GStr("value")),
  ])
  let _ = my_data
}
