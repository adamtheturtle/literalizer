defmodule Check do
  def x do
    my_var = %{
        "_" => "_",
    }
    item_var = %{
        "_" => "_",
    }
    my_data = %{
        "key" => my_var,
        "items" => [item_var, %{"fallback" => "value"}],
    }
    _ = my_data
  end
end
