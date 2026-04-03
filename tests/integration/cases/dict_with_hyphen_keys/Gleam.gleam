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
    #("my-key", GStr("value1")),
    #("another-key", GStr("value2")),
    #("normal_key", GStr("value3")),
  ])
  let _ = my_data
}
