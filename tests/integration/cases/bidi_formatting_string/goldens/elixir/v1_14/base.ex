defmodule Check do
  def x do
    my_data = %{
        "v" => "a\u202A\u202B\u202C\u202D\u202E\u2066\u2067\u2068\u2069b",
    }
    _ = my_data
  end
end
