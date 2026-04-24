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
pub fn process(_data: a) -> Nil { panic }

pub fn main() {
  let my_var = GList([
    GInt(1),
    GInt(2),
    GInt(3),
  ])
  process(my_var)
}
