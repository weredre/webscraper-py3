import requests
from bs4 import BeautifulSoup

form = "Form W-2"
URL = (
    "https://apps.irs.gov/app/picklist/list/priorFormPublication."
    "html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value="
    "" + form + "&isDescending=false"
)
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
min_year = 0
max_year = 0
for table_element in soup.select(".picklist-dataTable tr:has(td)"):  # <-- change the selector here
    form_number = table_element.find("td", class_="LeftCellSpacer")
    form_title = table_element.find("td", class_="MiddleCellSpacer")
    form_year = table_element.find("td", class_="EndCellSpacer")
    if form_number.text.strip() == form:
        print(form_number.text.strip())
        print(form_title.text.strip())
        print(form_year.text.strip())
        print()
    if int(form_year.text.strip()) > max_year:
        max_year = int(form_year.text.strip())
    if int(form_year.text.strip()) < min_year or min_year == 0:
        min_year = int(form_year.text.strip())


print(max_year)
print(min_year)
