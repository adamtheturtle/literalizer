defmodule ClientType_ do
  def fetch(_payload), do: nil
end
defmodule Check do
  def x do
    app = %{client: ClientType_}
    app.client.fetch("hello")
    app.client.fetch(42)
    app.client.fetch(true)
  end
end
