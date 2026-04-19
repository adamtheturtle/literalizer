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
  let my_data = JStr("2024-01-15T12:30:00+00:00")
  let _ = my_data
}
