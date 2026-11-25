pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // event time
    #("when", GStr("2024-01-15T12:34:56+00:00")),
  ])
  let _ = my_data
}
