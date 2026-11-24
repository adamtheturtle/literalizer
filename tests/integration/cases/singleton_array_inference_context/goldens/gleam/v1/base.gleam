pub type GVal {
  GNull
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("nil", GList([GList([GList([GList([GList([GList([GList([GList([GList([GNull])])])])])])])])])),
    #("empty", GList([GList([GList([GList([GList([GList([GList([GList([GList([GList([])])])])])])])])])])),
    #("siblings", GList([GList([GList([GList([GList([GList([GList([GList([GList([GList([GInt(4), GInt(5)])])])])])])])])])])),
  ])
  let _ = my_data
}
