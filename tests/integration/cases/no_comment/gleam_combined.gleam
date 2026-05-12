pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("message", GStr("no comment here")),
  ])
  let my_data = GDict([
    #("message", GStr("no comment here")),
  ])
  let _ = my_data
}
