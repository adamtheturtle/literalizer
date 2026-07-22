Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {{"missing", -1}, {"present", 1}},
        New Dictionary(Of String, Object) From {{"missing", 2}, {"present", 3}}
    }
End Module
