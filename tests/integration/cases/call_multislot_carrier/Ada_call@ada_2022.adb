with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val; Extra : A_Val) is begin null; end Process;
begin
    Process(value => AInt (1), extra => AStr ("hello"));
    Process(value => AStr ("two"), extra => ABool (False));
    Process(value => AFloat (3.5), extra => ANull);
end Main;
