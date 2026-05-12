defmodule ClientType_ do
  def fetch(_value), do: nil
end
defmodule AppType_ do
  def client, do: ClientType_
end
defmodule Check do
  def x do
    app = AppType_
    app.client.fetch("hello")
    app.client.fetch("world")
  end
end
