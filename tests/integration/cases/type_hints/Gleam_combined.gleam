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
    #("joined", GStr("2024-01-15")),
    #("last_login", GStr("2024-01-15T12:30:00+00:00")),
    #("avatar", GStr("48656c6c6f")),
  ])
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("age", GInt(30)),
    #("active", GBool(True)),
    #("score", GNull),
    #("joined", GStr("2024-01-15")),
    #("last_login", GStr("2024-01-15T12:30:00+00:00")),
    #("avatar", GStr("48656c6c6f")),
  ])
  let _ = my_data
}
