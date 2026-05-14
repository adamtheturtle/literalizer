defmodule Http_clientType_ do
  def fetch(_payload), do: nil
end
defmodule My_appType_ do
  def http_client, do: Http_clientType_
end
defmodule Check do
  def x do
    my_app = My_appType_
    my_app.http_client.fetch("hello")
    my_app.http_client.fetch(42)
    my_app.http_client.fetch(true)
  end
end
