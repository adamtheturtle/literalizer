pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("label", GStr("tag")),
    #("meta", GDict([])),
  ])
  let _ = my_data
}
