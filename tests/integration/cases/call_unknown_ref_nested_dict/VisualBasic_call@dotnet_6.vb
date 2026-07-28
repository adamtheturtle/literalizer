Imports System.Collections.Generic
Module Check
    Function process(data As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_list = New Dictionary(Of String, Object) From {
            {"unused", "value"}
        }
        process(New Object() {New Object() {New Dictionary(Of String, Object) From {{"inner", my_list}}}})
    End Sub
End Module
