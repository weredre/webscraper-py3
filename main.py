import requests
import os
import json
from bs4 import BeautifulSoup

form = "Form W-2 P"  # <-- input for form search
first_year = 2012  # <-- input for first year for range pdf download
last_year = 2021  # <-- input for last year for range pdf download
years_to_download = range(first_year, last_year+1, 1)  # <-- range for pdf download
URL = (
    "https://apps.irs.gov/app/picklist/list/priorFormPublication."
    "html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value="
    "" + form + "&isDescending=false"
)
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
min_year = 0
max_year = 0

for table_element in soup.select(".picklist-dataTable tr:has(td)"):  # <-- selecting only the table rows that have td
    form_number = table_element.find("td", class_="LeftCellSpacer")
    form_title = table_element.find("td", class_="MiddleCellSpacer")
    form_year = table_element.find("td", class_="EndCellSpacer")
    if form_number.text.strip() == form:  # <-- if statement to match correct tax form
        data_form_number = form_number.text.strip()
        data_form_title = form_title.text.strip()
    if int(form_year.text.strip()) > max_year:  # <-- getting correct max year
        max_year = int(form_year.text.strip())
    if int(form_year.text.strip()) < min_year or min_year == 0:   # <-- getting correct min year
        min_year = int(form_year.text.strip())
    if form_number.text.strip() == form and int(form_year.text.strip()) in years_to_download:   # <-- download pdf
        u = form_number.a["href"]
        p = "{}-{}.pdf".format(
            form_number.get_text(strip=True), form_year.get_text(strip=True)
        )

        path = os.path.join(form, p)

        if not os.path.exists(form):
            os.makedirs(form)

        print(f"Saving {u=} to {path=}")
        with open(path, "wb") as f_out:
            f_out.write(requests.get(u).content)

data = {'tax_form': []}
data['tax_form'].append({
    'Form_Number': data_form_number,
    'Form_Title': data_form_title,
    'Min_Year': min_year,
    'Max_Year': max_year
})
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
