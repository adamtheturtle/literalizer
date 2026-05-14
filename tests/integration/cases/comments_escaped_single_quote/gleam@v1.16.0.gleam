pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("key", GStr("it's here")),  // a comment
  ])
  let _ = my_data
}
