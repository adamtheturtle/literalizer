pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // before	line
    #("value", GStr("left\tright")),  // inline	line
    // after	line
  ])
  let _ = my_data
}
