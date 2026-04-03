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
    // Server configuration
    #("host", GStr("localhost")),  // default host
    #("port", GInt(8080)),
    // Enable debug mode
    #("debug", GBool(True)),
  ])
  let _ = my_data
}
