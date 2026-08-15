defmodule Check do
  def x do
    my_data = "a\u0085b\u2028c\u2029d\r\u2028e"
    _ = my_data
  end
end
