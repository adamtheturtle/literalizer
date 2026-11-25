<?php
class ClientType { function go($first_value, $second_value) {} }
class AppType { public $client; function __construct() { $this->client = new ClientType(); } }
$app = new AppType();
$app->client->go(first_value: [1], second_value: ["text"]);
