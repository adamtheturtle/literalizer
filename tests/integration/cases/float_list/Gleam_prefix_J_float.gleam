pub type GVal {
  JNull
  JBool(Bool)
  JInt(Int)
  JFloat(Float)
  JStr(String)
  JList(List(GVal))
  JDict(List(#(String, GVal)))
  JSet(List(GVal))
}

pub fn main() {
  let my_data = JList([
    JFloat(1.1),
    JFloat(-2.2),
    JFloat(3.3),
  ])
  let _ = my_data
}
