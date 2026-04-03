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
    #("key", GStr("value \" # not a comment")),  // real
  ])
  let my_data = GDict([
    #("key", GStr("value \" # not a comment")),  // real
  ])
  let _ = my_data
}
