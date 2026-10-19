pub type GVal {
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([
      GDict([
        #("mapping", GDict([])),
      ]),
      GDict([]),
    ]),
    GList([
      GDict([]),
      GDict([
        #("mapping", GDict([])),
      ]),
    ]),
  ])
  let _ = my_data
}
