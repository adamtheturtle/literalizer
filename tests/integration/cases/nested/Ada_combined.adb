with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("users", AList'[AMap'[AEntry ("name", AStr ("Bob")), AEntry ("tags", AList'[AStr ("admin"), AStr ("user")])], AMap'[AEntry ("name", AStr ("Carol")), AEntry ("tags", AList'[AStr ("guest")])]])
    ];
begin
    my_data := AMap'[
        AEntry ("users", AList'[AMap'[AEntry ("name", AStr ("Bob")), AEntry ("tags", AList'[AStr ("admin"), AStr ("user")])], AMap'[AEntry ("name", AStr ("Carol")), AEntry ("tags", AList'[AStr ("guest")])]])
    ];
end Check;
