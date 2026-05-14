with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AStr ("ADD"), AStr ("alice"), AStr ("hello")],
        AList'[AStr ("DEL"), AStr ("bob"), AStr ("5")]  -- removes "world"
    ];
begin
    my_data := AList'[
        AList'[AStr ("ADD"), AStr ("alice"), AStr ("hello")],
        AList'[AStr ("DEL"), AStr ("bob"), AStr ("5")]  -- removes "world"
    ];
end Main;
