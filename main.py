from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


URL = 'https://gulp.de/'
CHROME_PATH = '/usr/local/bin/chromedriver'


def find_projects(search_query, is_headless):
    if is_headless:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
    else:
        chrome_options = None


    driver = webdriver.Chrome(executable_path=CHROME_PATH, options=chrome_options)  # Optional argument, if not specified will search path.
    driver.get(URL)
    find(driver, 'onetrust-accept-btn-handler', By.ID)\
        .click()
    find(driver, "//*[@id='content']/div[1]/div[1]/div[2]/form/div[1]/input[2]") \
        .send_keys(search_query)
    find(driver, "//*[@id='content']/div[1]/div[1]/div[2]/form/div[2]/button") \
        .click()

    page = 1
    found_projects = []
    while True:
        project_links = find_objects(driver, "//app-project-view/div/div/div[2]/h2/a")

        for link in project_links:
            found_projects.append(link.text)

        next_button = find(driver, "//a[@class='next']")
        if next_button.find_element(By.XPATH, "..").get_attribute("class") != "disabled":
            page += 1
            print("waiting page %d to open..." % page)
            next_button.click()
            find(driver, build_page_link_path(page))
            print("next page is obtained!")
        else:
            break

    driver.quit()
    return found_projects


def build_page_link_path(page_number):
    return "//app-paginated-list[@class='ng-star-inserted']/app-paginator/div/div/ul/div/li[*][" \
           "@class='ng-star-inserted active']/a[text()=%d]" % page_number


def find(driver, query, search_method=By.XPATH, wait=True):
    print("searching for element", query)
    if wait:
        return WebDriverWait(driver, 10).until(EC.presence_of_element_located((search_method, query)))
    else:
        return driver.find_element(search_method, query)


def find_objects(driver, query, search_method=By.XPATH):
    print("searching for element", query)
    return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((search_method, query)))


if __name__ == '__main__':
    projects = find_projects("java", True)
    print("\nRESULTS:")
    print("\n".join(projects))
    print("Total %d projects!" % len(projects))