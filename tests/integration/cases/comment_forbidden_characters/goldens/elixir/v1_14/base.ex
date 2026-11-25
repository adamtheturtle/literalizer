defmodule Check do
  def x do
    my_data = %{
        "a" => 1,  # tab	here and bidi <U+202E>after
        "b" => 2,
    }
    _ = my_data
  end
end
