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
    #("1", GStr("one")),
    #("2", GStr("two")),
    #("42", GStr("answer")),
  ])
  let my_data = GDict([
    #("1", GStr("one")),
    #("2", GStr("two")),
    #("42", GStr("answer")),
  ])
  let _ = my_data
}
