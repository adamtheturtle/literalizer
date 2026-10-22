structure app = struct
structure client = struct
fun consume _ = ()
end
end
val _ = app.client.consume({x = 1}, 2)
val _ = app.client.consume({name = "Ada"}, 3)
