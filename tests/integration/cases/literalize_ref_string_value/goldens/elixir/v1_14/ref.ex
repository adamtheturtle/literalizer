defmodule Check do
  def x do
    shared = "s"
    my_data = %{
        "value" => shared,
    }
    _ = my_data
  end
end
