import boto3
import time
from selenium import webdriver
from findElements import ElementFinder


def launch_browser():
    chromedriver_path = '/Users/calvin/Downloads/chromedriver'
    driver = webdriver.Chrome(executable_path=chromedriver_path)

    driver.get("https://www.instagram.com/accounts/login/")
    return driver

driver = launch_browser()

Finder = ElementFinder(driver=driver)



def login():

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

    notNow= Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]")
    notNow.click()



def searchUser(target):

    searchInput = Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/input")
    searchInput.send_keys(target)

    firstUser = Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a")
    firstUser.click()
    

    firstPost=Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a")
    if firstPost != None:
        firstPost.click()

        likeButton= Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button/div[2]/span/svg")
        likeButton.click()

        xButton = Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/svg")
        xButton.click()

        secondPost=Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[2]/a")
        if secondPost != None:
            secondPost.click()

            likeButton= Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button/div[2]/span/svg")
            likeButton.click()

            xButton = Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/svg")
            xButton.click()    

        thirdPost=Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[3]/a")
        if thirdPost != None:
            thirdPost.click()    


            likeButton= Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button/div[2]/span/svg")
            likeButton.click()

            xButton = Finder.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/svg")
            xButton.click()    


login()
searchUser("meganeroberts")

# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'https://sqs.us-west-1.amazonaws.com/649237903886/SpartanIGBot'


cont=True
while cont:
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        VisibilityTimeout=0,
        WaitTimeSeconds=20
    )

    if 'Messages' in response:
        noResponseCount=0
        print("processing")
        message = response['Messages'][0]
        
        receipt_handle = message['ReceiptHandle']
        messageBody = message['Body']

        searchUser(messageBody)

        
        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

    else:
        noResponseCount+=1
        if noResponseCount==5:
            cont=False
        print("no response, count:", noResponseCount)

     