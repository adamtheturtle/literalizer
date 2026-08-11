defmodule Check do
  def x do
    foo = %{
        "_" => "_",
    }
    my_data = %{
        "mapping" => %{"value" => foo},
        "items" => [%{"other" => 1}, foo],
    }
    _ = my_data
  end
end
