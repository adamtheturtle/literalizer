with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AMap'[AEntry ("$ref", AStr ("my_str"))]]
    ];
begin
    my_data := AList'[
        AList'[AMap'[AEntry ("$ref", AStr ("my_str"))]]
    ];
end Main;
