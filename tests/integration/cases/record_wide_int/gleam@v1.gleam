pub type GVal {
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("quantity", GInt(1000000)),
    #("big", GInt(18446744073709551615)),
    #("ratio", GFloat(2.5)),
    #("label", GStr("tag")),
    #("ok", GBool(True)),
  ])
  let _ = my_data
}
