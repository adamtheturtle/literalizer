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
    #("outer", GDict([#("a", GInt(1)), #("b", GStr("x")), #("c", GNull)])),
  ])
  let _ = my_data
}
