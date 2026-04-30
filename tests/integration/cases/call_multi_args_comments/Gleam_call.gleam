pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_ts: a, _start: b, _end: c) -> Nil { Nil }

pub fn main() {
  process(GInt(1), GInt(0), GInt(3600))  // Jan 1 1970 00:00:00 - 01:00:00
  process(GInt(5), GInt(0), GInt(3600))  // Jan 1 1970 00:00:05 - 01:00:05
  process(GInt(2), GInt(0), GInt(5400))  // Jan 1 1970 00:00:02 - 01:30:02
}
