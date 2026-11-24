defmodule ApiType_ do
  def fetch(_data), do: nil
end
defmodule Check do
  def x do
    process = %{api: ApiType_}
    process.api.fetch(%{"data" => "hello"})
    process.api.fetch(%{"data" => 42})
    process.api.fetch(%{"data" => true})
  end
end
