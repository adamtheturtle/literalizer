pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("url", GStr("https://example.org/a/*b*/")),
    #("count", GInt(2)),
  ])
  let _ = my_data
}
