pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("single_map", GList([GDict([])])),
    #("single_list", GList([GList([GInt(1)])])),
    #("single_deep", GList([GList([GList([GInt(2)])])])),
  ])
  let _ = my_data
}
