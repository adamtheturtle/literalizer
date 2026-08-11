defmodule Check do
  def x do
    foo = %{
        "_" => "_",
    }
    my_data = %{
        "items" => [%{"other" => 1}, foo],
        "mapping" => %{"value" => foo},
    }
    _ = my_data
  end
end
