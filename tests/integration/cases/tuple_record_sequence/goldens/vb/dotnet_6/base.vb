Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {{"call", "send"}, {"args", New Object() {1, "email", "a@gmail.com", 100}}},
        New Dictionary(Of String, Object) From {{"call", "recv"}, {"args", New Object() {2, "sms", "b@example.com", 200}}}
    }
End Module
