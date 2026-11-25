defmodule Check do
  def x do
    my_data = %{
        "a" => {4294967296, 4294967297},
    }
    _ = my_data
  end
end
