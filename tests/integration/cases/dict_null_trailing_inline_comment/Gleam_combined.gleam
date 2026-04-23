pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
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
