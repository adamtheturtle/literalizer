defmodule ClientType_ do
  def fetch(_payload), do: nil
end
defmodule AppType_ do
  def client, do: ClientType_
end
defmodule Check do
  def emit(_arg), do: nil
  def x do
    app = AppType_
    emit(app.client.fetch("hello"))
    emit(app.client.fetch(42))
    emit(app.client.fetch(true))
  end
end
