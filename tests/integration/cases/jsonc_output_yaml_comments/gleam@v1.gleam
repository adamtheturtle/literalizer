pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // server
    #("host", GStr("localhost")),  // default
  ])
  let _ = my_data
}
