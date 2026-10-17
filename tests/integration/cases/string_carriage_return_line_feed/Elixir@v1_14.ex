defmodule Check do
  def x do
    my_data = %{
        "cr" => "a\rb",
        "crlf" => "a\r\nb",
        "lf" => "a\nb",
    }
    _ = my_data
  end
end
