defmodule ClientType_ do
  def go(_first_value, _second_value), do: nil
end
defmodule Check do
  def x do
    app = %{client: ClientType_}
    app.client.go([1], ["text"])
  end
end
