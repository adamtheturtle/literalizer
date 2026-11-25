defmodule Check do
  def x do
    item_var = %{
        "_" => "_",
    }
    my_data = %{
        "items" => [item_var, %{"fallback" => "value"}],
    }
    _ = my_data
  end
end
