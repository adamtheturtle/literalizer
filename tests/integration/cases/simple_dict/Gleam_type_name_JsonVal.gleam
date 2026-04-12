pub type JsonVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(JsonVal))
  GDict(List(#(String, JsonVal)))
  GSet(List(JsonVal))
}

pub fn main() {
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("age", GInt(30)),
    #("active", GBool(True)),
    #("score", GNull),
  ])
  let _ = my_data
}
