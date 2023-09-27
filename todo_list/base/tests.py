from django.test import TestCase, Client
from django.urls import reverse
from base.models import TaskContainer, Task
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


from playwright.sync_api import sync_playwright
from django.test import LiveServerTestCase
from django.urls import reverse

from bs4 import BeautifulSoup
import os
import sys


# class GetIntoPageTest(LiveServerTestCase):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=50)
#         page = browser.new_page()
#         page.goto('localhost:8000/login/')
#         page.fill('input#username', 'Aleks')
#         page.fill('input#password', 'Aleks2003')
#         page.get_by_role("button", name="Login").click()
#         page.is_visible('.login-logout-div') # wait untill certain component or something is visible
#         html = page.inner_html('.container-div')
#         print(html)
#         print('HTML ENDS HERE ----------------------------------------')
#         soup = BeautifulSoup(html, 'html.parser')
#         print(soup.find_all('h3'))
#         print('soup 1 ends here ========================================')
#         total_orders = soup.find('h3', {'class': 'user-name'}).text
#         print(f'user-name is:{total_orders}')
    # page.click('button[type=submit]')


# class GetIntoPageTest(LiveServerTestCase):

#     def test_login_and_check_html(self):
#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=False, slow_mo=50)
#             page = browser.new_page()
#             page.goto(self.live_server_url + '/login/')  # Use self.live_server_url to access the local test server URL
#             page.fill('input#username', 'Aleks')
#             page.fill('input#password', 'Aleks2003')
#             page.get_by_role("button", name="Login").click()
#             page.wait_for_selector('.login-logout-div')  # Wait for an element with the specified selector to appear
#             html = page.inner_html('.container-div')
#             print(html)
#             print('HTML ENDS HERE ----------------------------------------')
#             soup = BeautifulSoup(html, 'html.parser')
#             print(soup.find_all('h3'))
#             print('soup 1 ends here ========================================')
#             total_orders = soup.find('h3', {'class': 'user-name'}).text
#             print(f'user-name is:{total_orders}')
#             self.assertTrue("Expected text" in total_orders)  # Add your assertions here as needed


# class RegisterUserInPageTest(TestCase, StaticLiveServerTestCase):

#     def setUp(self):
#         super().setUp()
#         self.playwright = sync_playwright().start()
#         self.browser = self.playwright.chromium.launch(headless=False, slow_mo=500)


#     def tearDown(self):
#         super().tearDown()
#         self.browser.close()
#         self.playwright.stop()

#     def test_register_user(self):
#         page = self.browser.new_page()
#         page.goto(f"{self.live_server_url}/register/")
#         page.fill('input#id_username', 'Toni')
#         page.fill('input#id_password1', 'Toni123!')
#         page.fill('input#id_password2', 'Toni123!')
#         page.get_by_role('button', name='Register').click()

#         current_url = page.url
#         print(current_url)
#         expected_url = self.live_server_url + reverse('container_list')
#         print(expected_url)
#         self.assertEqual(current_url, expected_url)

class MyFunctionalTest(TestCase, StaticLiveServerTestCase):

    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     print("this is class setup")
    #     cls.browser = None

    # @classmethod
    # def tearDownClass(cls):
    #     if cls.browser:
    #         cls.browser.close()
    #     super().tearDownClass()
    #     print("this is class teardown")

    def setUp(self):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUp()
        print('this is setup')
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False, slow_mo=1000)
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/register/")
        page.get_by_label("Username:").fill("test")
        page.get_by_label("Password:", exact=True).fill("test123!")
        page.get_by_label("Confirm Password:").fill("test123!")
        page.get_by_role("button", name="Register").click()

    def tearDown(self):
        super().tearDown()
        print('this is teardown')
        self.browser.close()
        self.playwright.stop()
    
    def test_login_with_container(self):
        from base.models import TaskContainer
        user, create = User.objects.get_or_create(username='test')

        container = TaskContainer.objects.create(
            user=user,
            title='Test123123123'
        )

        container.save()

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/login/")
        page.get_by_label("Username:").fill("test")
        page.get_by_label("Password:").fill("test123!")
        page.get_by_role("button", name="Login").click()
        

    def test_login_without_containers(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/login/")
        page.get_by_label("Username:").fill("test")
        page.get_by_label("Password:").fill("test123!")
        page.get_by_role("button", name="Login").click()



# class UserTestCase(TestCase, StaticLiveServerTestCase):
#     def setUp(self):
#             # os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
#             self.playwright = sync_playwright().start()
#             self.browser = self.playwright.chromium.launch(headless=False, slow_mo=2500)
#             self.username = 'test'
#             self.email = 'testuser@example.com'
#             self.password = 'test123!'
#             self.user = User.objects.create_superuser(self.username, self.email, self.password)

#     def tearDown(self):
#             super().tearDown()
#             self.browser.close()
#             self.playwright.stop()

#     def test_create_superuser(self):
#             self.assertEqual(self.user.username, self.username)
#             self.assertEqual(self.user.email, self.email)
#             self.assertTrue(self.user.check_password(self.password))
#             self.assertTrue(self.user.is_superuser)
#             self.assertTrue(self.user.is_staff)

#     def test_login_superuser(self):
#             page = self.browser.new_page()
#             page.goto(f"{self.live_server_url}/admin/")
#             page.wait_for_selector('text=Django administration')
#             page.get_by_label("Username:").fill("test")
#             page.get_by_label("Password:").fill("test123!")
#             page.get_by_role("button", name="Log in").click()
            
        
    # def test_superuser_registration(self):
    #     # Create a superuser
    #     user = User.objects.create_superuser(
    #         username='admin',
    #         password='adminpassword',
    #         email='admin@example.com'
    #     )

    #     # Check if the user is a superuser
    #     self.assertTrue(user.is_superuser)
    #     self.assertTrue(user.is_staff)

    #     # Check if the user can log in
    #     self.client.login(username='admin', password='adminpassword')

    #     # Check if the login was successful
    #     response = self.goto(f"{self.live_server_url}/admin/")  # Replace with your admin URL
    #     self.assertEqual(response.status_code, 200)
    
    # def test_login(self):
    #     page = self.browser.new_page()
    #     page.goto(f"{self.live_server_url}/admin/")
    #     page.wait_for_selector('text=Django administration')
    #     page.fill('[name=username]', 'Aleks')
    #     page.fill('[name=password]', 'Aleks2003')
    #     page.click('text=Log in')

    #     page.wait_for_selector('text=Django administration')
    #     self.assertIn('/admin/', page.url())


        
        # assert len(page.eval_on_selector(".errornote", "el => el.innerText")) > 0
        # page.close()

        # if 'python3 manage.py test' in sys.argv:
        #     print("this is working in command")
        # else:
        #     print("this could still be working")


    # def test_login_user(self):

# class MyViewTests(StaticLiveServerTestCase):

#     def setUp(self):
#         super().setUp()
#         self.playwright = sync_playwright().start()
#         self.browser = self.playwright.chromium.launch(headless=False, slow_mo=500)

#     def tearDown(self):
#         super().tearDown()
#         self.browser.close()
#         self.playwright.stop()

#     def test_login(self):
#         page = self.browser.new_page()
#         page.goto(f"{self.live_server_url}/admin/")
#         page.wait_for_selector('text=Django administration')
#         page.fill('[name=username]', 'myuser')
#         page.fill('[name=password]', 'secret')
#         page.click('text=Log in')
#         assert len(page.eval_on_selector(".errornote", "el => el.innerText")) > 0
#         page.close()



# class LoginEndToEndTest(TestCase, StaticLiveServerTestCase):
#     def setUp(self):
#         super().setUp()
#         with sync_playwright() as p:
#             self.page = p.chromium.launch()

#     def tearDown(self):
#         self.page.close()
#         self.browser.close()

#     def test_login_successful(self):
#         pass
#         page = self.page

#         try:
#             # Navigate to the login page
#             page.goto(self.live_server_url + reverse('login'))

#             # Fill in the login form
#             page.fill('input[name="username"]', 'Aleks')
#             page.fill('input[name="password"]', 'Aleks2003')

#             # Click the login button
#             page.click('.btn-login')

#             # Wait for navigation to complete
#             page.wait_for_load_state('networkidle')

#             # Check if the user is redirected to the expected page after successful login
#             self.assertEqual(page.url, self.live_server_url + reverse('container_list'))
#         except Exception as e:
#             self.fail(f"Error in test_login_successful: {str(e)}")

#     def test_login_unsuccessful(self):
#         page = self.page

#         # Navigate to the login page
#         page.goto(self.live_server_url + reverse('login'))

#         # Fill in the login form with incorrect password
#         page.fill('input[name="username"]', 'Tonton')
#         page.fill('input[name="password"]', 'incorrect')

#         # Click the login button
#         page.click('.loggin-button')

#         # Wait for navigation to complete
#         page.wait_for_load_state('networkidle')

#         # Check if the user is still on the login page (unsuccessful login)
#         self.assertEqual(page.url, self.live_server_url + reverse('login'))




# class TaskContainerTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='asd')
#         print("its now setup")

#     def tearDown(self):
#         self.user.delete()
#         print("its now deleted")

#     def test_task_container_creation(self):
#         self.container = TaskContainer.objects.create(user=self.user, title='Test Task Container')

#         saved_task_container = TaskContainer.objects.get(pk=self.container.pk)

#         self.assertEqual(saved_task_container.user, self.user)
#         self.assertEqual(saved_task_container.title, 'Test Task Container')

#     def test_create_task_in_container(self):
#         self.test_task_container_creation()

#         self.task = Task.objects.create(
#             user=self.user,
#             container=self.container,
#             title="This is a test task", 
#             description="test desc",
#         )

#         print(f"user: {self.task.user}, container title: {self.task.container.title}, task: {self.task.title}, description: {self.task.description}" )

#         saved_task = Task.objects.get(pk=self.task.pk)
        
#         self.assertTrue(self.task.due is None)
#         self.assertEqual(saved_task.user, self.user)
#         self.assertEqual(saved_task.container, self.container)
#         self.assertEqual(saved_task.title, "This is a test task")

#     def test_task_container_without_user(self):
#         task_container = TaskContainer.objects.create(title='Test Task Container')

#         saved_task_container = TaskContainer.objects.get(pk=task_container.pk)

#         self.assertIsNone(saved_task_container.user, "There is no user")
#         self.assertEqual(saved_task_container.title, 'Test Task Container')

        # self.assertIn('form', response.context)
        # self.assertTemplateUsed(response, 'login.html', )

# class LoginTestCase(TestCase, StaticLiveServerTestCase):
#     def setUp(self):
#         self.username = "Tonton"
#         self.email = "tonzo@mailinator.com"
#         self.password = "Test123!@#"
#         self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

#     def tearDown(self):
#         self.user.delete()


#     def test_login_successful(self):
#         url = reverse('login')
#         response = self.client.get(url)
#         response_post = self.client.post(url, {'username':self.username, 'password':self.password})
#         self.assertRedirects(response_post, reverse("container_list"))
#         self.assertTrue(self.user.is_authenticated)

#         self.assertEqual(200, response.status_code)
#         self.assertTemplateUsed(response, "base/login.html")
        
#     def test_login_unsuccessful(self):
#         url = reverse('login')
#         response = self.client.post(url, {'username':self.username, 'password':'incorrect'})

#         self.assertEqual(200, response.status_code)
#         self.assertFalse(response.wsgi_request.user.is_authenticated)




    # def test_login_authenticated_user_get_request(self):
    #     login_user = self.client.login(username='Tonton', password='Test123!@#')

    #     print(login_user)
        
        
        
        # self.assertFalse(user.is_valid())
        
        
        
        # self.client.force_login(user)
