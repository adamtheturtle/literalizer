Imports System.Collections.Generic
Module Check
    Function process(data As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_var = 42
        Dim my_other = 7
        process(New Object() {New Dictionary(Of String, Object) From {{"ref", "my_var"}}, 42, "static"})
        process(New Object() {New Dictionary(Of String, Object) From {{"ref", "my_other"}}, 7, "label"})
    End Sub
End Module
