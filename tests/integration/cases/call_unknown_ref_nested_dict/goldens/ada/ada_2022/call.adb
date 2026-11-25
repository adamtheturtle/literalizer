with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val) is begin null; end Process;
    my_list : A_Val := AMap'[
        AEntry ("unused", AStr ("value"))
    ];
begin
    Process(data => AList'[AList'[AMap'[AEntry ("inner", my_list)]]]);
end Main;
