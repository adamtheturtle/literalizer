pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("s", GStr("string")),
    #("i", GInt(1)),
    #("f", GFloat(1.5)),
    #("b", GBool(True)),
    #("n", GNull),
    #("d", GStr("2024-01-15")),
    #("dt", GStr("2024-01-15T12:00:00")),
    #("by", GStr("48656c6c6f")),
  ])
  let _ = my_data
}
