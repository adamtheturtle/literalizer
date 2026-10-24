pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("b", GDict([#("k", GInt(1))])),
    #("a", GDict([#("k", GStr("2040-01-01T00:00:00+00:00"))])),
  ])
  let _ = my_data
}
