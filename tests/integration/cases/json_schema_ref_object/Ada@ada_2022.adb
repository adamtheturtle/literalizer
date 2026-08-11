with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("schema", AMap'[AEntry ("$ref", AStr ("#/defs/Foo"))])
    ];
begin
    null;
end Main;
