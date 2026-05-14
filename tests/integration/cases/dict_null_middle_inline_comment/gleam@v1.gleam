pub type GVal {
  GNull
  GBool(Bool)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("host", GStr("localhost")),
    #("port", GNull),  // not configured yet
    #("debug", GBool(True)),
  ])
  let _ = my_data
}
