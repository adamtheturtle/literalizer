defmodule Check do
  def make_widget(_count), do: nil
  def x do
    my_data = "${"${"// payload"}"}" // trailing
    // extra
    _ = my_data
  end
end
