Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        ' Test cases
        process(New Dictionary(Of String, Object) From {{"type", "create"}, {"pr_id", "pr_1"}})  ' first case
        process(New Dictionary(Of String, Object) From {{"type", "update"}, {"pr_id", "pr_2"}})  ' second case
        ' third case
        process(New Dictionary(Of String, Object) From {{"type", "delete"}, {"pr_id", "pr_3"}})
    End Sub
End Module
