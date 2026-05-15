pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("host", GStr("it's here")),  // a comment
    #("port", GInt(80)),  // another
  ])
  let my_data = GDict([
    #("host", GStr("it's here")),  // a comment
    #("port", GInt(80)),  // another
  ])
  let _ = my_data
}
