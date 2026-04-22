<?php
class ClientType { function post($data) {} }
class ApiType { public $client; function __construct() { $this->client = new ClientType(); } }
class ObjType { public $api; function __construct() { $this->api = new ApiType(); } }
$obj = new ObjType();
$obj->api->client->post(data: "hello");
$obj->api->client->post(data: 42);
$obj->api->client->post(data: true);
