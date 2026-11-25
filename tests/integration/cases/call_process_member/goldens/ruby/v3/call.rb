class ProcessType; def fetch(*a, **kw); end; end
class AppType; def process; ProcessType.new; end; end
app = AppType.new
app.process.fetch(data: {"data" => "hello"})
app.process.fetch(data: {"data" => 42})
app.process.fetch(data: {"data" => true})
