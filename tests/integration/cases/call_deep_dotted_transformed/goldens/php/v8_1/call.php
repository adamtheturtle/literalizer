<?php
class ClientType { function fetch($payload) {} }
class AppType { public $client; function __construct() { $this->client = new ClientType(); } }
$app = new AppType();
function emit($_arg) {}
emit($app->client->fetch(payload: "hello"));
emit($app->client->fetch(payload: 42));
emit($app->client->fetch(payload: true));
