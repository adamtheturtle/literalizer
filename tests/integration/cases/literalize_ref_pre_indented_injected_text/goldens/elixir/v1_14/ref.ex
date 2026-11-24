defmodule Check do
  def x do
                shared = [
                    1,
                    2,
                ]
                other = 3
                payload = "\n    shared : Val\nshared = RInt 99"
                my_data = %{
                    "a" => shared,
                    "b" => other,
                    "payload" => payload,
                }
    _ = my_data
  end
end
