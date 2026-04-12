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
    JFloat(todo),
    JFloat(todo),
    JFloat(todo),
  ])
  let _ = my_data
}
