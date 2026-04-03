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
    #("name", GStr("Alice")),
    #("scores", GDict([#("1", GStr("first")), #("2", GStr("second"))])),
  ])
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("scores", GDict([#("1", GStr("first")), #("2", GStr("second"))])),
  ])
  let _ = my_data
}
