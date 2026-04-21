<?php
class ApiType { function request($data) {} }
class ClientType { public $api; function __construct() { $this->api = new ApiType(); } }
$client = new ClientType();
client.api.request(data: "hello");
client.api.request(data: 42);
client.api.request(data: true);
