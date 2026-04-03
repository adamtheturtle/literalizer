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
    #("age", GInt(30)),
    #("active", GBool(True)),
    #("score", GNull),
  ])
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("age", GInt(30)),
    #("active", GBool(True)),
    #("score", GNull),
  ])
  let _ = my_data
}
