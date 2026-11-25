defmodule Check do
  def x do
    shared = "a\0b"
    my_data = %{
        "value" => shared,
    }
    _ = my_data
  end
end
