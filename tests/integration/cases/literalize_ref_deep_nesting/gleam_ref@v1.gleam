pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let deep = GList([
    GList([
      GStr("one"),
      GStr("two"),
    ]),
    GList([
      GStr("three"),
      GStr("four"),
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
