<?php
class ClientType { function fetch($payload) {} }
class AppType { public $client; function __construct() { $this->client = new ClientType(); } }
$app = new AppType();
$app->client->fetch(payload: "hello");
$app->client->fetch(payload: 42);
$app->client->fetch(payload: true);
