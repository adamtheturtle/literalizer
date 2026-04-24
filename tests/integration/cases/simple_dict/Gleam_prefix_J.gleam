pub type GVal {
  JNull
  JBool(Bool)
  JInt(Int)
  JStr(String)
  JDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = JDict([
    #("name", JStr("Alice")),
    #("age", JInt(30)),
    #("active", JBool(True)),
    #("score", JNull),
  ])
  let _ = my_data
}
