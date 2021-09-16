# spiritmco

This project aimed to automate the sourcing of potential job candidates for Spirit Consulting. The program pulls information from LinkedIn pages, searches the. Apollo.io database, then extracts the candidate's email. It accepts parameters of a usual LinkedIn Recruiter search (industry, position, company size, etc.) as well as desired number of candidates returned. The output is a CSV file with candidates that fit the given parameters (e.g. 'Healthcare', 'CXO', '10k+ employees')

Tried two methods to make the program usable for Spirit employees without Python
1) Use Google Cloud App Run to publish simple web application
2) Use Tkinter to create GUI executable 

Script works well locally, but in both instances the application could not reconnect to the webdriver (I am using the Selenium geckodriver)
