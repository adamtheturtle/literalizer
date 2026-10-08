pub type GVal {
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("d", #(GDict([#("a", #(GDict([#("b", #(GInt(1), #(GFloat(2.5), #(GStr("x"), #(GBool(True))))))])))]))),
  ])
  let _ = my_data
}
