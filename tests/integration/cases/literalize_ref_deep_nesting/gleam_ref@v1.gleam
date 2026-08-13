pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let deep = GList([
    GList([
      GInt(1),
      GInt(2),
    ]),
    GList([
      GInt(3),
      GInt(4),
    ]),
  ])
  let my_data = GDict([
    #("a", GDict([
      #("b", GDict([
        #("c", deep),
      ])),
    ])),
  ])
  let _ = my_data
}
