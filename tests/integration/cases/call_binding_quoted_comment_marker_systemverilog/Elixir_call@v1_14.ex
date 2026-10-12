defmodule Check do
  def make_widget(_text), do: nil
  def x do
    my_data = make_widget("first \"quote\"\n// string body") // note
    // extra
    _ = my_data
  end
end
