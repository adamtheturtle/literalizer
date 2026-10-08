defmodule Check do
  def x do
    my_data = %{
        "x" => "before\0after",
    }
    _ = my_data
  end
end
