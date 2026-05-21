pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let userObj = GDict([
    #("_", GStr("_")),
  ])
  let my_data = userObj
  let _ = my_data
}
