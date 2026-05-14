pub type GVal {
  GNull
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // comment
    #("name", GStr("Alice")),
    #("score", GNull),
  ])
  let _ = my_data
}
