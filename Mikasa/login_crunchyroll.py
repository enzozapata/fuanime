from selenium import webdriver
import codecs
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By

# Creamos una nueva instancia del driver PhantomJS
driver = webdriver.PhantomJS()

# nos dirigimos al login de crunchyroll
driver.get("http://www.crunchyroll.com/login")

# Aca nos para Cloudflare, mostramos el titulo de la pagina:
print driver.title
# El tipico Just a moment...
# Asi que hacemor una espera explicita, que espere hasta que aparezca el formulario de logueo (By.ID, "login_form_name")
element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "login_form_name")))
# Llamamos al campo name del formulario como nick
nick = driver.find_element_by_name("login_form[name]")

# Con send_keys escribimos o subimos archivos, etc, depende del tipo de input
nick.send_keys("crunchyuser")
# El campo password
password = driver.find_element_by_name("login_form[password]")
# Le mandamos la password
password.send_keys("crunchypass")
# Enviamos
nick.submit()

try:
    # Hacemos una espera implicita de 5 segundos
    driver.implicitly_wait(5)
    # Mostramos el titulo
    print driver.title
	# Guardamos las cookies en cookies
    cookies = driver.get_cookies()
    file = codecs.open("cukiss.txt", "r+", "utf-8-sig")
    for i in range(0,len(cookies)):
        file.write(cookies[i]["name"]+"="+cookies[i]["value"]+";\n") 
    file.close()
    driver.implicitly_wait(1)
    driver.get("http://crdx.org/misc/cookies/")
    itdomain = driver.find_element_by_id("domain")
    itdomain.clear()
    itdomain.send_keys("crunchyroll.com")
    driver.implicitly_wait(2)
    itinput = driver.find_element_by_id("input")
    itinput.clear()
    file2 = codecs.open("cukiss.txt", "r+", "utf-8-sig")
    itinput.send_keys(file2.read())
    driver.implicitly_wait(2)
    btngenerate = driver.find_element_by_id("generate")
    btngenerate.click()
    driver.implicitly_wait(2)
    itoutput = driver.find_element_by_id("output").get_attribute('value')
    print itoutput
    file2.close()
    file3 = codecs.open("cookie.txt","r+", "utf-8-sig") 
    file3.write("# Netscape HTTP Cookie File")
    file3.write("# http://curl.haxx.se/rfc/cookie_spec.html")
    file3.write("# This is a generated file!  Do not edit.")
    file3.write(itoutput)
    file3.close()
finally:
    driver.quit()
raw_input()
