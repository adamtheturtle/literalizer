defmodule Check do
  def x do
    my_data = %{
        "outer" => [%{"_" => 1}],
    }
    _ = my_data
  end
end
