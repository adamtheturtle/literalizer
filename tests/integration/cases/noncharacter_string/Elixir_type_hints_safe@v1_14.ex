defmodule Check do
  def x do
    my_data = %{
        "fffe" => "￾",
        "ffff" => "￿",
    }
    _ = my_data
  end
end
