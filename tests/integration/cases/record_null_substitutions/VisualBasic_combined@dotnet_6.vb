Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"rows", New Object() {New Dictionary(Of String, Object) From {{"replacement", Nothing}, {"present", 1}}, New Dictionary(Of String, Object) From {{"replacement", 2}, {"present", 3}}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"rows", New Object() {New Dictionary(Of String, Object) From {{"replacement", Nothing}, {"present", 1}}, New Dictionary(Of String, Object) From {{"replacement", 2}, {"present", 3}}}}
        }
    End Sub
End Module
