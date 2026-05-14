<?php
class ClientType { function fetch($value) {} }
class AppType { public $client; function __construct() { $this->client = new ClientType(); } }
$app = new AppType();
$app->client->fetch(value: "hello");
$app->client->fetch(value: "world");
