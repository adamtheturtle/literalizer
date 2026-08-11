with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("schema", AMap'[AEntry ("$ref", AStr ("#/defs/Foo"))])
    ];
begin
    my_data := AMap'[
        AEntry ("schema", AMap'[AEntry ("$ref", AStr ("#/defs/Foo"))])
    ];
end Main;
