from django.test import TestCase, Client
import json
#from .import 

# django manage.py test .ProjectEndpoint


# Create your tests here.
#http://localhost:8044/login/
#
# Create user
#
# username: 9849298499
# password: 1onepiece
#
# login with that user
#
# check login success
# check invalid login

"""
mysite/urls.py:349:    re_path(r'^api/login/', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)),       
mysite/urls.py:352:    path('login/', login_view, name="login"),  
"""
def loadJson(path):
    with open(path, 'r',encoding="utf8") as f:
        return json.loads(f.read())

class TestAccount(TestCase):
    # def test_account_model(self):
    #     obj = Account.objects.create(
            
    #     )

    """
    import data from some file,
        eg: test_account_login_data={'username':u, 'pw': p}
    def test_func():
        test_acc= import.test_account_login_data;
        client.post('route', test_acc)
    """

    def test_browser_account_login(self):
        data = {'username':'9849298499', 'password': '1onepiece'}
        data = loadJson('account/tests/data_login.json')
        print(data)

        c = Client() #above, from django.test import TestCase,Client
        #optional, but may be necessary for your configuration: c.login("username","password")
        response = c.post('/',params=data) #login bhanne route chaina
        #print(response._container) # output data

        self.assertNotEqual(response.status_code, 200) #invalid pw 200 ???
        #self.assertEqual(response.status_code, 301)
        #self.assertEqual("a", "b") # compare two things
        #self.assertEqual(response.status_code, 200)
    
    def test_account_register(self): # this didnot work (with 2 classes)
        #E:\job\cp\hmsHospitalMngSys\hms\src\account\views.py
        #RegisterAPI(APIView):
        #
        return
        data={
            'mobile': '1234567890',
            'password': '!@#$qwerasdf',
            'email': 'test@email.com',
            #'username': mobile,
            'firstname': 'firstname',
            'lastname': 'lastname'
        }
        c=Client()
        response = c.post('/api/register', params=data)
        #print(response.__dict__)
        self.assertEqual(response.status_code, 200)
        #todo: complete this, 




"""
The following code inserted at the beginning of the testcase creates a user, logs them in, and allows the rest of the test to contiue

self.user = User.objects.create_user(username='testuser', password='12345')
login = self.client.login(username='testuser', password='12345')

https://stackoverflow.com/questions/36940384/how-do-i-setup-a-unit-test-user-for-django-app-the-unit-test-cant-login
"""


"""
http://localhost:8000/register/
    didnot work

re_path(r'^api/register/', RegisterAPI.as_view(), name="register"),
account.views
class RegisterAPI(APIView):
@csrf_exempt
	def post

"""