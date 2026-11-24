pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn thing_go(_before: a, _populated: b, _after: c) -> Nil { Nil }

pub fn main() {
  let _ = thing_go(GList([]), GList([GInt(1)]), GList([]))
  let _ = thing_go(GList([GStr("text")]), GList([GInt(2)]), GList([]))
  let _ = thing_go(GList([]), GList([GStr("text")]), GList([]))
  let _ = thing_go(GList([GStr("text")]), GList([GInt(2)]), GList([GInt(3)]))
}
