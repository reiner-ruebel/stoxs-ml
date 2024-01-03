class RegisterResult:
    def yes():
        return {'success': True, 'message': "yes"}
    def no():
        return {'success': False, 'message': "no"}
        