proc app.client.fetch {args} {return {}}
proc emit {args} {}
emit [app.client.fetch "hello"]
emit [app.client.fetch 42]
emit [app.client.fetch 1]
