structure app = struct
structure client = struct
fun consume _ = ()
end
end
val _ = app.client.consume()
