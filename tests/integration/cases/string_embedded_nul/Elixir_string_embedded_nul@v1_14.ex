defmodule Check do
  def x do
    my_data = %{
        "x" => "\0",
        "y" => "\01",
    }
    _ = my_data
  end
end
