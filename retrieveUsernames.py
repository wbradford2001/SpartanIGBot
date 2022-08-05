import boto3

from selenium import webdriver
from findElements import ElementFinder


def handler(event):
    def launch_browser():
        chromedriver_path = '/Users/calvin/Downloads/chromedriver'
        driver = webdriver.Chrome(executable_path=chromedriver_path)

        driver.get("https://www.instagram.com/" + str(event["targetUser"]))
        return driver

    driver = launch_browser()

    Finder = ElementFinder(driver=driver)

    with open('username.txt') as f:
        USER = f.read().strip()
        username = Finder.find_element_by_name('username')
        username.send_keys(USER)


    with open('password.txt') as f:
        PASS = f.read().strip()
        password = Finder.find_element_by_name('password')
        password.send_keys(PASS)

    submit = Finder.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button")
    submit.click()

    saveInfo = Finder.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button")
    saveInfo.click()

    notNow= Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]", wait=6)
    if notNow != None:
        notNow.click()

    searchInput = Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/input")
    searchInput.send_keys("hihi")

    firstUser = Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a")
    firstUser.click()

    followers = Finder.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/button")
    followers.click()


    while True:
        pass




    userNames = ["First", "Second", "Third","Fourth","Fifth","Sixth"]


    # Create SQS client
    sqs = boto3.client('sqs')

    queue_url = 'https://sqs.us-west-1.amazonaws.com/649237903886/SpartanIGBot'

    # Send message to SQS queue
    for userName in userNames:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=(
                userName
            )
        )



event={"targetUser": "meganeroberts"}
handler(event)