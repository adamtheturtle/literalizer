$Foo = @{
    "_" = "_"
}
$my_data = @{
    "items" = @(@{"other" = 1}; $Foo);
    "mapping" = @{"value" = $Foo}
}
