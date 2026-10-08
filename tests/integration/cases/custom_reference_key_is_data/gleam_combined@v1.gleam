pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("reference", GStr("whole")),
  ])
  let my_data = GDict([
    #("reference", GStr("whole")),
  ])
  let _ = my_data
}
