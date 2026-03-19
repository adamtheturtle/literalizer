Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"users", New Object() {New Dictionary(Of String, Object) From {{"name", "Bob"}, {"tags", New String() {"admin", "user"}}}, New Dictionary(Of String, Object) From {{"name", "Carol"}, {"tags", New String() {"guest"}}}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"users", New Object() {New Dictionary(Of String, Object) From {{"name", "Bob"}, {"tags", New String() {"admin", "user"}}}, New Dictionary(Of String, Object) From {{"name", "Carol"}, {"tags", New String() {"guest"}}}}}
        }
    End Sub
End Module
