defmodule Check do
  def x do
    my_var = %{
        "_" => "_",
    }
    my_data = %{
        "key" => my_var,
    }
    _ = my_data
  end
end
