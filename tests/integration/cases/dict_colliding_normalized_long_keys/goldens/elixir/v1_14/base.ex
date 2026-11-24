defmodule Check do
  def x do
    my_data = %{
        "a_b" => 1,
        "a-b" => 2,
        "averyveryverylongkeynamethatgoesonandonandon" => 3,
        "averyveryverylongkeynamethatgoesonandmore" => 4,
    }
    _ = my_data
  end
end
