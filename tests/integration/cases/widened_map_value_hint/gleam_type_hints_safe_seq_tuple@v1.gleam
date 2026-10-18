pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = #(
    GDict([#("a", GInt(1))]),
    GInt(1),
    GStr("x"),
    GBool(True),
    GFloat(2.5),
    GNull,
  )
  let _ = my_data
}
