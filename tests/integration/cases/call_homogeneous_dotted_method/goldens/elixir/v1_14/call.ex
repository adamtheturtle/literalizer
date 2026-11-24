defmodule ClientType_ do
  def fetch(_value), do: nil
end
defmodule Check do
  def x do
    app = %{client: ClientType_}
    app.client.fetch("hello")
    app.client.fetch("world")
  end
end
