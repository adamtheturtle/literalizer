#!/usr/bin/env escript
%% Compile and execute golden modules without changing their declared names.
%% Binary output also permits 255-character module atoms whose .beam filename
%% would exceed the filesystem's component limit.

main([PathsFile]) ->
    {ok, Contents} = file:read_file(PathsFile),
    Paths = binary:split(Contents, <<0>>, [global, trim_all]),
    Results = [run(binary_to_list(Path)) || Path <- Paths],
    case lists:member(error, Results) of
        true -> halt(1);
        false -> halt(0)
    end.

run(Path) ->
    io:format("RUN: ~ts~n", [Path]),
    Options = [binary, warnings_as_errors, report_errors, report_warnings],
    case compile:file(Path, Options) of
        {ok, Module, Beam} ->
            try
                {module, Module} = code:load_binary(Module, Path, Beam),
                _ = Module:x(),
                ok
            catch Kind:Reason:Stack ->
                io:format("FAIL ~ts: ~p:~p~n~p~n", [Path, Kind, Reason, Stack]),
                error
            end;
        error -> error
    end.
