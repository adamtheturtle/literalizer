pub type GVal {
  GNull
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("host", GStr("localhost")),
    #("port", GNull),  // not configured yet
  ])
  let my_data = GDict([
    #("host", GStr("localhost")),
    #("port", GNull),  // not configured yet
  ])
  let _ = my_data
}
