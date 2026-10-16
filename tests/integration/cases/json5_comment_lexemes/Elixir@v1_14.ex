defmodule Check do
  def x do
    my_data = %{
        # heading
        "a" => "single ' // data",
        "b" => "linecontinuation",
        "c" => "\\",  # actual comment
        "d" => "\u2028\u2029",  # final comment
    }
    _ = my_data
  end
end
