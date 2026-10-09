defmodule Check do
  def x do
    text = "a\u202Ab"
    my_data = %{
        "value" => text,
    }
    _ = my_data
  end
end
