defmodule Check do
  def x do
    my_data = %{
        "a_b" => 0o1,
        "a-b" => 0o2,
        "averyveryverylongkeynamethatgoesonandonandon" => 0o3,
        "averyveryverylongkeynamethatgoesonandmore" => 0o4,
    }
    _ = my_data
  end
end
