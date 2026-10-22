Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {{"outer", New Dictionary(Of String, Object) From {{"inner", New Dictionary(Of String, Object) From {{"x", 1}}}}}},
        New Dictionary(Of String, Object) From {{"outer", New Dictionary(Of String, Object) From {{"inner", New Dictionary(Of String, Object) From {}}}}}
    }
End Module
