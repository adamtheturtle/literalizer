pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("numbers", GList([GInt(1), GInt(2)])),
    #("nested", GDict([#("inner", GList([GInt(3)]))])),
    #("mixed", GList([GInt(4), GStr("five")])),
  ])
  let _ = my_data
}
