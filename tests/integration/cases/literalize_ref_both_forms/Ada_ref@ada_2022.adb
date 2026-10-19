with A_Stub; use A_Stub;
procedure Main is
    shared_values : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
    my_data : A_Val := AMap'[
        AEntry ("a", shared_values)
    ];
begin
    my_data := AMap'[
        AEntry ("a", shared_values)
    ];
end Main;
