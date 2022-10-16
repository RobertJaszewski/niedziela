import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.relative_locator import locate_with
from faker import Faker
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# PARAMETRY TESTU

GRID_HUB_URL = "http://127.0.0.1/wd/hub"

# DANE TESTOWE
email = "testinggeeko@gmail.com"
nazwisko = "Kowalski"
haslo = "test12@"

class RejestracjaNowegoUzytkownika(unittest.TestCase):
    def setUp(self):
        # WARUNKI WSTĘPNE
        # 1. Otwarta przeglądarka
        #self.driver = webdriver.Chrome()
        self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.EDGE)
        self.driver.maximize_window()
        # 2. Otwarta strona główna
        self.driver.get("https://www.eobuwie.com.pl/")
        # 3. Użytkownik niezalogowany
        # Zamknij alert o ciasteczkach
        self.driver.find_element(By.CLASS_NAME,"e-button--type-primary.e-button--color-brand.e-consents-alert__button.e-button").click()
        self.fake = Faker()
    def testBrakPodaniaImienia(self):
        sleep(2)
        # 1. Kliknij "zarejestruj"
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Zarejestruj").click()
        # 2. Wpisz nazwisko
        lastName = self.driver.find_element(By.ID, "lastname")
        lastName.send_keys(self.fake.last_name())
        # 3. Wpisz adres e-mail
        adres = self.driver.find_element(By.ID, "email_address")
        adres.send_keys(email)
        # 4. Wpisz hasło (co najmniej 6 znaków)
        passwordInput = self.driver.find_element(By.ID, "password")
        passwordInput.send_keys(haslo)
        # 5. Wpisz ponownie hasło w celu potwierdzenia
        passwordConfirmation = self.driver.find_element(By.ID, "confirmation")
        passwordConfirmation.send_keys(haslo)
        # 6. Zaznacz „ Oświadczam, że zapoznałem się z treścią Regulaminu serwisu i akceptuję
        #  jego postanowienia.”
        checkboxStatement = self.driver.find_element(By.XPATH, '//label[@class="checkbox-wrapper__label"]').click()
        # OSTROŻNIE!!!
        # 7. Kliknij „Załóż nowe konto” (tylko dla przypadków niegatywnych!)
        createNewAccount = self.driver.find_element(By.XPATH, '//button[@data-testid="register-create-account-button"]').click()

        ### OCZEKIWANY REZULTAT ###
        # Użytkownik otrzymuje informację, "To pole jest wymagane" pod imieniem
        # 1. Szukam pola imię
        poleImie = self.driver.find_element(By.NAME, "firstname")
        # 2. Szukam spana z błędem przy pomocy 2 metod
        error_span = self.driver.find_element(locate_with(By.XPATH, '//span[@class="form-error"]').near(poleImie))
        error_span2 = self.driver.find_element(locate_with(By.XPATH, '//span[@class="form-error"]').above(lastName))
        #Sprawdzam, czy obie metody wskazują ten sam element

        self.assertEqual(error_span.id, error_span2.id) # assertEqual
        # 3. Sprawdzam, czy jest tylko jeden taki span
        errory = self.driver.find_elements(By.XPATH, '//span[@class="form-error"]')
        liczba_errorow = len(errory)
        self.assertEqual(liczba_errorow, 1)
        # 4. Sprawdzam, czy treść tegoż spana brzmi "To pole jest wymagane" pod imieniem
        bledny_error = "To pole jest wymaganee"
        self.assertEqual(error_span.text, "To pole jest wymagane")

    def tearDown(self):
        sleep(6)
        #zakończenie testu
        self.driver.quit()

        #Warunek końcowy:
        # 1. Konto nie jest założone

# Jeśli uruchamiam z tego pliku
if __name__ == '__main__':
    # to uruchom testy
    unittest.main()