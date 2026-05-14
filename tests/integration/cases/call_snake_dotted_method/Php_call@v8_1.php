<?php
class Http_clientType { function fetch($payload) {} }
class My_appType { public $http_client; function __construct() { $this->http_client = new Http_clientType(); } }
$my_app = new My_appType();
$my_app->http_client->fetch(payload: "hello");
$my_app->http_client->fetch(payload: 42);
$my_app->http_client->fetch(payload: true);
