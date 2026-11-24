
Val := [
    RInt(I128),
    RList(List(Val)),
]
main! = |_args| {
    created = Playlist(RInt(1.I128))
    expect created == Playlist(RInt(1.I128))
    Ok({})
}
