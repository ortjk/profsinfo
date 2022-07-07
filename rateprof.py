from selenium.webdriver.common.by import By
import time
import useful_functions


# this is a function which takes a list of names in the format [[surname0, name0], [surname1, name1], ...], the name of
# a university, a subject, and a selenium webdriver. it will then go to the website 'ratemyprofessors.com' and search
# for and collect information on the input names. it then returns a list of dicts, which can easily be used by pandas to
# create a dataframe.
def prof_searcher(names, school_name, subject, driver):
    total_teacher_data = []

    driver.get('https://www.ratemyprofessors.com/search/')
    # close cookies popup
    driver.implicitly_wait(2)
    driver.find_element(By.CLASS_NAME, 'FullPageModal__StyledCloseIcon-sc-1tziext-0').click()

    # enter school name and click on the first autofill result
    elem = driver.find_elements(By.CLASS_NAME, 'Search__DebouncedSearchInput-sc-10lefvq-1')[1]
    driver.implicitly_wait(1)
    useful_functions.enter_text_in_field(school_name, elem, driver, enter=False)
    driver.find_element(By.CLASS_NAME, 'TypeaheadItemList__StyledTypeaheadItemList-sc-1veot99-0').click()

    for i in names:
        # enter the name into the search bar
        elem = driver.find_element(By.CLASS_NAME, 'Search__DebouncedSearchInput-sc-10lefvq-1')
        driver.implicitly_wait(2)
        useful_functions.enter_text_in_field(i[1] + ' ' + i[0], elem, driver)

        # first, get the number of results. for each result, then go through each result individually. a somewhat
        # complicated while loop is needed, as a simple for loop through 'current_teacher_options' will not work.
        # this is because once the first result is examined, attempting to go to the next one is impossible as it is
        # then a 'stale element'. so, a new list of results is required every time.
        current_teacher_options = driver.find_elements(By.CLASS_NAME, 'TeacherCard__StyledTeacherCard-syjs0d-0')
        _ = 0
        while _ < len(current_teacher_options):
            p = driver.find_elements(By.CLASS_NAME, 'TeacherCard__StyledTeacherCard-syjs0d-0')[_]

            # check if the result has ratings, teaches the subject, and is not from a different school than entered
            if '0 ratings' not in p.text and subject in p.text and 'other schools' not in driver.find_element(By.CLASS_NAME, 'SearchResultsPage__SearchResultsPageHeader-vhbycj-3').text:
                driver.execute_script("arguments[0].click();", p)

                # show more results if possible
                while driver.find_elements(By.CLASS_NAME, 'Buttons__Button-sc-19xdot-1'):
                    driver.find_element(By.CLASS_NAME, 'Buttons__Button-sc-19xdot-1').click()
                    # needed for load time
                    time.sleep(1)

                # the dict which the information is written to
                categories = {
                    "Name": i[0] + ', ' + i[1],
                    # ratings
                    '5.0': 0,
                    '4.5': 0,
                    '4.0': 0,
                    '3.5': 0,
                    '3.0': 0,
                    '2.5': 0,
                    '2.0': 0,
                    '1.5': 0,
                    '1.0': 0,
                    "Take Again?": "",
                    "Level of Difficulty": "",
                    # class info
                    "Classes": [],
                    "Most Recent Review": "",
                    # tag count
                    "Tough Grader": 0,
                    "Would Take Again": 0,
                    "Get Ready To Read": 0,
                    "Participation Matters": 0,
                    "Extra Credit": 0,
                    "Group Projects": 0,
                    "Amazing Lectures": 0,
                    "Clear Grading Criteria": 0,
                    "Gives Good Feedback": 0,
                    "Inspirational": 0,
                    "Lots Of Homework": 0,
                    "Hilarious": 0,
                    "Beware Of Pop Quizzes": 0,
                    "So Many Papers": 0,
                    "Caring": 0,
                    "Respected": 0,
                    "Lecture Heavy": 0,
                    "Test Heavy": 0,
                    "Graded By Few Things": 0,
                    "Accessible Outside Class": 0,
                    "Online Savvy": 0,
                    "Tests Are Tough": 0,
                    "Skip Class? You Wont Pass.": 0
                }

                categories['Take Again?'] += driver.find_elements(By.CLASS_NAME, 'FeedbackItem__FeedbackNumber-uof32n-1')[0].text
                categories['Level of Difficulty'] += driver.find_elements(By.CLASS_NAME, 'FeedbackItem__FeedbackNumber-uof32n-1')[1].text
                categories['Most Recent Review'] += driver.find_elements(By.CLASS_NAME, 'RatingHeader__RatingTimeStamp-sc-1dlkqw1-3')[1].text

                # specify items from the list of reviews only
                focus = driver.find_element(By.CLASS_NAME, 'RatingsList__RatingsUL-hn9one-0')
                # get tags
                for q in focus.find_elements(By.CLASS_NAME, 'Tag-bs9vf4-0'):
                    # use the tag itself as an index (some text formatting is required)
                    categories[q.text.replace("'", '').lower().title()] += 1

                # get class names
                for q in focus.find_elements(By.CLASS_NAME, 'RatingHeader__StyledClass-sc-1dlkqw1-2'):
                    if q.text != '':
                        categories['Classes'].append(q.text)

                # get ratings (double increment is needed as quality and difficulty use the same classes)
                _1 = 0
                q = focus.find_elements(By.CLASS_NAME, 'CardNumRating__CardNumRatingNumber-sc-17t4b9u-2')
                while _1 < len(q):
                    categories[q[_1].text] += 1

                    _1 += 2

                total_teacher_data.append(categories)
                driver.back()
                driver.implicitly_wait(1)
            _ += 1

    return total_teacher_data
