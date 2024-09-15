from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import unittest


def create_driver():
    
    # Set up Microsoft Edge WebDriver options
    edge_options = Options()
    edge_options.add_argument("--start-maximized")

    # Specify the path to Microsoft Edge WebDriver
    webdriver_service = EdgeService('./msedgedriver.exe')  # Replace with the actual path to msedgedriver
    return webdriver.Edge(service=webdriver_service, options=edge_options)



class LoginSignupTest(unittest.TestCase):
    def setUp(self):
        self.driver = create_driver()
        self.wait = WebDriverWait(self.driver, 180, poll_frequency=5)

    def tearDown(self):
        self.driver.close()

    def test_login(self):
        return
        # Open your web page
        self.driver.get("http://127.0.0.1:5000/login?next=%2Flogout#")
        email = self.wait.until(EC.element_to_be_clickable((By.ID, 'email-login')))
        email.send_keys("danielakalamudo@gmail.com")
        sleep(2)
        
        
        password = self.wait.until(EC.element_to_be_clickable((By.ID, 'password-login')))
        password.send_keys("password")
     
   
        sign_in_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'login-button')))
        sign_in_button.click()
        sleep(2)
        self.assertIn("Choose a starting place", self.driver.page_source)

    def test_signup(self):
        return
        self.driver.get("http://127.0.0.1:5000/login?next=%2Flogout#")
        signup_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.signUp-link')))
        signup_link.click()
        data = {
                        "email-signup": "danielakalamudo2208@gmail.com",

            "Firstname": "Daniel",
            "Lastname": "AKalamudo",
            "password-signup": "password",
            "password-confirm-signup": "password"
        }
        for key, value in data.items():
            input_field = self.wait.until(EC.element_to_be_clickable((By.ID, key)))
            input_field.send_keys(value)
            sleep(2)
        sign_up_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'signup-submit')))
        sign_up_button.click()
        sleep(10)
        self.assertIn("Choose a starting place", self.driver.page_source)

class RouteOptimizationTest(unittest.TestCase):
    def setUp(self):
        self.driver = create_driver()
        self.wait = WebDriverWait(self.driver, 10)
    def tearDown(self):
        self.driver.close()
    

    def test_route_optimization(self):
        self.driver.get("http://127.0.0.1:5000/login?next=%2Flogout#")
        email = self.wait.until(EC.element_to_be_clickable((By.ID, 'email-login')))
        email.send_keys("danielakalamudo@gmail.com")
        sleep(2)
        
        
        password = self.wait.until(EC.element_to_be_clickable((By.ID, 'password-login')))
        password.send_keys("password")
     
   
        sign_in_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'login-button')))
        sign_in_button.click()
        sleep(5)
        self.assertIn("Choose a starting place", self.driver.page_source)
        # Open the weights dropdown
        self.driver.find_element(By.ID, "weights-dropdown-button").click()
        sleep(1)  # Allow the dropdown to become visible

        # Fill out the weights form
        mode_select = self.driver.find_element(By.ID, "mode-select")
        mode_select.send_keys("Cycling")
    
        self.driver.find_element(By.ID, "time-weight").clear()
        self.driver.find_element(By.ID, "time-weight").send_keys("3")
    
        self.driver.find_element(By.ID, "distance-weight").clear()
        self.driver.find_element(By.ID, "distance-weight").send_keys("5")
    
        self.driver.find_element(By.ID, "calories-weight").clear()
        self.driver.find_element(By.ID, "calories-weight").send_keys("2")
    
        self.driver.find_element(By.ID, "carbon-weight").clear()
        self.driver.find_element(By.ID, "carbon-weight").send_keys("4")
    
        self.driver.find_element(By.ID, "noise-weight").clear()
        self.driver.find_element(By.ID, "noise-weight").send_keys("1")
    
        self.driver.find_element(By.ID, "scenic-weight").clear()
        self.driver.find_element(By.ID, "scenic-weight").send_keys("6")
    
        self.driver.find_element(By.ID, "aqi-weight").clear()
        self.driver.find_element(By.ID, "aqi-weight").send_keys("7")
    
        self.driver.find_element(By.ID, "safety-weight").clear()
        self.driver.find_element(By.ID, "safety-weight").send_keys("8")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        sleep(2)
        # Select starting place
        origin_input = self.driver.find_element(By.CSS_SELECTOR, "#mapbox-directions-origin-input input")
        origin_input.click()
        origin_input.send_keys("London")
        sleep(2)
    
        # Wait for suggestions to appear and select the first one (if needed)
        suggestions = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.suggestions :first-child")))
        suggestions.click()

        # Select destination place
        
        destination_input = self.driver.find_element(By.CSS_SELECTOR, "#mapbox-directions-destination-input input")
        destination_input.click()
        destination_input.send_keys("coventry")
        sleep(2)
    
        # Wait for suggestions to appear and select the first one (if needed)
        suggestions = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.suggestions :first-child")))
        suggestions.click()
    
       
    
        # Submit the weights form

    
        # Verify map interaction (ensure the selected mode is updated)
        sleep(180)
        self.wait.until(EC.element_to_be_clickable((By.ID, "route-summary")))
    
    

        # Optionally, check for the presence of optimized routes
        route_summary = self.driver.find_element(By.ID, "route-summary").text
        self.assertIn("Route Label", route_summary)


if __name__ == "__main__":
    unittest.main()