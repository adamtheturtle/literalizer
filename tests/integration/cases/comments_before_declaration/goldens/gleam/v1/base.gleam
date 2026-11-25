pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // Configuration
    #("name", GStr("app")),
    // Port setting
    #("port", GInt(3000)),
  ])
  let _ = my_data
}
