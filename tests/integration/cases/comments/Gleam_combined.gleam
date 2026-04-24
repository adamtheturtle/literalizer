pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // Server configuration
    #("host", GStr("localhost")),  // default host
    #("port", GInt(8080)),
    // Enable debug mode
    #("debug", GBool(True)),
  ])
  let my_data = GDict([
    // Server configuration
    #("host", GStr("localhost")),  // default host
    #("port", GInt(8080)),
    // Enable debug mode
    #("debug", GBool(True)),
  ])
  let _ = my_data
}
