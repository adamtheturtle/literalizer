pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let my_list = GDict([
    #("unused", GStr("value")),
  ])
  process(GList([GList([GDict([#("inner", my_list)])])]))
}
