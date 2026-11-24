pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub type Playlist { Playlist(GVal) }
pub fn main() {

let created = Playlist(GInt(1))
  let assert Playlist(GInt(1)) = created
  Nil
}
