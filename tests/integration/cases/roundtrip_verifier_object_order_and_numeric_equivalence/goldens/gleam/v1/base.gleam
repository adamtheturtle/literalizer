pub type GVal {
  GNull
  GBool(Bool)
  GFloat(Float)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("b", GNull),
    #("a", GDict([#("y", GList([GFloat(1.0)])), #("x", GBool(False))])),
  ])
  let _ = my_data
}
