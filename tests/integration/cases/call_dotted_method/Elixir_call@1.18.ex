defmodule ClientType_ do
  def fetch(_payload), do: nil
end
defmodule AppType_ do
  def client, do: ClientType_
end
defmodule Check do
  def x do
    app = AppType_
    app.client.fetch("hello")
    app.client.fetch(42)
    app.client.fetch(true)
  end
end
