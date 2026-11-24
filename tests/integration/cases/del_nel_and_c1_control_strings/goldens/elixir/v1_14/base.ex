defmodule Check do
  def x do
    my_data = %{
        "del" => "ab",
        "nel" => "a\u0085b",
        "c1" => "ab",
    }
    _ = my_data
  end
end
