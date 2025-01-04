class BaseResource:
    def get(self, request):
        raise NotImplementedError("GET method not implemented.")

    def post(self, request):
        raise NotImplementedError("POST method not implemented.")

    def put(self, request):
        raise NotImplementedError("PUT method not implemented.")

    def delete(self, request):
        raise NotImplementedError("DELETE method not implemented.")

