defmodule ClientType_ do
  def fetch(_payload), do: nil
end
defmodule Check do
  def emit(_arg), do: nil
  def x do
    app = %{client: ClientType_}
    emit(app.client.fetch("hello"))
    emit(app.client.fetch(42))
    emit(app.client.fetch(true))
  end
end
