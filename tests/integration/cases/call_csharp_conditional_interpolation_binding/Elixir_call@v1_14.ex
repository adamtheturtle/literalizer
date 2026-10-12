defmodule Check do
  def make_widget(_count), do: nil
  def x do
    my_data = $"{(true ? "// payload" : "ok")}" // trailing
    // extra
    _ = my_data
  end
end
