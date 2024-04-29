from flask import jsonify


class Error:
    def __new__(self, status, error):
        self.status = status
        self.error = error
        return jsonify({"Status": self.status, "Message": self.error})
