defmodule Check do
  def x do
    my_data = %{
        "a" => 1,
        "b" => 1_099_511_627_776,
    }
    _ = my_data
  end
end
