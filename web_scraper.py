import requests
import bs4
import lxml
import csv

#HTTP request
response = requests.get("https://techdayhq.com/new-york/participants")
soup = bs4.BeautifulSoup(response.text, "lxml")

with open ("csv.csv", "w") as csvFile:
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["Grouping", "Company Name", "Tech Day URL", "Social Profiles URLs", "Company Description", "Company URL"])

    grouping = ""

    for div in soup.select(".main .main .section div"):
        cssClasses = div["class"]

        for cssClass in cssClasses:
            #reset the variable values
            companyName = ""
            techDayURL = "https://techdayhq.com"
            links = []
            companyDescription = ""
            companyURL = ""

            #if the div contains a title of a new section
            if "section-heading" in cssClass:
                grouping = div.findAll(text=True)[0].strip()
            #if the div contains a company details
            elif "company" in cssClass:
                techDayURL += div.a["href"]
                companyName = div.select(".name")[0].text

                #HTTP request for techDayURL of the company
                companyPageResponse = requests.get(techDayURL)
                companySoup = bs4.BeautifulSoup(companyPageResponse.text, "lxml")

                for socialMediaLink in companySoup.select(".social-icons > a"):
                    links.append(socialMediaLink["href"])

                companyDescription = companySoup.select(".description > p")[0].text

                urlList = companySoup.select(".company-url > a")

                #some companies don't have their company url, so getting the 0th index is not possible
                if len(urlList) > 0:
                       companyURL = urlList[0]["href"]

                #write to the csv file
                csvWriter.writerow([grouping, companyName, techDayURL, ",".join(links), companyDescription, companyURL])
