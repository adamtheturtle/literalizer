pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let existing = GDict([
    #("_", GStr("_")),
  ])
  let my_data = existing
  let _ = my_data
}
