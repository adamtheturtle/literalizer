defmodule ProcessType_ do
  def fetch(_data), do: nil
end
defmodule Check do
  def x do
    app = %{process: ProcessType_}
    app.process.fetch(%{"data" => "hello"})
    app.process.fetch(%{"data" => 42})
    app.process.fetch(%{"data" => true})
  end
end
