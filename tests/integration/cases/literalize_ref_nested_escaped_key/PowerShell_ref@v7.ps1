$Foo = @{
    "_" = "_"
}
$my_data = @{
    "mapping" = @{"value" = $Foo};
    "items" = @(@{"other" = 1}; $Foo)
}
