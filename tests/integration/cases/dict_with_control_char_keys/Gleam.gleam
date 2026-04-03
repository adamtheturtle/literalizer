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
    #("key\nwith\nnewlines", GStr("value1")),
    #("key\twith\ttabs", GStr("value2")),
    #("", GStr("value3")),
  ])
  let _ = my_data
}
