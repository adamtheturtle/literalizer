with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("my-key", AStr ("value1")),
        AEntry ("another-key", AStr ("value2")),
        AEntry ("normal_key", AStr ("value3"))
    ];
begin
    null;
end Main;
