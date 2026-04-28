with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("key", AStr ("value "" # not a comment"))  -- real
    ];
begin
    my_data := AMap'[
        AEntry ("key", AStr ("value "" # not a comment"))  -- real
    ];
end Main;
