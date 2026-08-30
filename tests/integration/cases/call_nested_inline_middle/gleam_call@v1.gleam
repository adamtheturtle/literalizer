pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn f(_ops: a) -> Nil { Nil }

pub fn main() {
  f(GList([GList([GStr("DEL"), GStr("b"), GStr("10")]), GList([GStr("ADD"), GStr("a"), GStr("x")])]))  // note
  // next call
  f(GList([GList([GStr("ADD"), GStr("c"), GStr("y")])]))
}
