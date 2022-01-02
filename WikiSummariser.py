import base64
import random
import urllib.request

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from RepositoryForObject import ObjectRepository
from selenium.webdriver.common.by import By
import pandas as pd

from mongoDBOperations import MongoDBManagement

import wikipedia

class WikiSummariser:

    def __init__(self, executable_path, chrome_options):
        """
        This function initializes the web browser driver
        :param executable_path: executable path of chrome driver.
        """
        try:
            self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initializing the webdriver object.\n" + str(e))

    def waitExplicitlyForCondition(self, element_to_be_found):
        """
        This function explicitly for condition to satisfy
        """
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
            WebDriverWait(self.driver, 2, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, element_to_be_found)))
            return True
        except Exception as e:
            return False

    def getCurrentWindowUrl(self):
        """
        This function returns the url of current window
        """
        try:
            current_window_url = self.driver.current_url
            return current_window_url
        except Exception as e:
            raise Exception(f"(getCurrentWindowUrl) - Something went wrong on retrieving current url.\n" + str(e))

    def getLocatorsObject(self):
        """
        This function initializes the Locator object and returns the locator object
        """
        try:
            locators = ObjectRepository()
            return locators
        except Exception as e:
            raise Exception(f"(getLocatorsObject) - Could not find locators\n" + str(e))

    def findElementByXpath(self, xpath):
        """
        This function finds the web element using xpath passed
        """
        try:
            element = self.driver.find_element(By.XPATH, value=xpath)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByXpath) - XPATH provided was not found.\n" + str(e))

    def findElementByClass(self, classpath):
        """
        This function finds web element using Classpath provided
        """
        try:
            element = self.driver.find_element(By.CLASS_NAME, value=classpath)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByClass) - ClassPath provided was not found.\n" + str(e))

    def findElementsBytag(self, tag_name):
        """
        This function finds web element using tag_name provided
        """
        try:
            element = self.driver.find_elements_by_tag_name(tag_name)
            return element
        except Exception as e:
            raise Exception(f"(findElementsByTag) - ClassPath provided was not found.\n" + str(e))
            
            
    def findElementsByTag(self,tag_name,Path1):
        """
        This function finds web element using tag_name provided
        """
        try:
            element = Path1.find_elements(By.TAG_NAME,value=tag_name)
            return element
        except Exception as e:
            raise Exception(f"(findElementsByTag) - ClassPath provided was not found.\n" + str(e))

    def findElementByTag(self, tag_name):
        """
        This function finds web element using Classpath provided
        """
        try:
            element = self.driver.find_element(By.TAG_NAME,value=tag_name)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByTag) - ClassPath provided was not found.\n" + str(e))

    def findElementByTag(self, tag_name,temp_a):
        """
        This function finds web element using Classpath provided
        """
        try:
            element = temp_a.find_element(By.TAG_NAME,value=tag_name)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByTag) - ClassPath provided was not found.\n" + str(e))

    def findElementsByCSS(self, selector_name,temp_object1):
        """
        This function finds web element using Classpath provided
        """
        try:
            element = temp_object1.find_elements(By.CSS_SELECTOR,value=selector_name)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementsByCSS) - ClassPath provided was not found.\n" + str(e))

    def findingElementsFromPageUsingClass(self, element_to_be_searched):
        """
        This function finds all element from the page.
        """
        try:
            result = self.driver.find_elements(By.CLASS_NAME, value=element_to_be_searched)
            return result
        except Exception as e:
            raise Exception(
                f"(findingElementsFromPageUsingClass) - Something went wrong on searching the element.\n" + str(e))

    def findingElementsFromPageUsingCSSSelector(self, element_to_be_searched):
        """
        This function finds all element from the page.
        """
        try:
            result = self.driver.find_elements(By.CSS_SELECTOR, value=element_to_be_searched)
            return result
        except Exception as e:
            raise Exception(
                f"(findingElementsFromPageUsingClass) - Something went wrong on searching the element.\n" + str(e))

    def openUrl(self, url):
        """
        This function open the particular url passed.
        :param url: URL to be opened.
        """
        try:
            if self.driver:
                self.driver.get(url)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(openUrl) - Something went wrong on opening the url {url}.\n" + str(e))


    def searchProduct(self, searchString):
        """
        This function helps to search product using search string provided by the user
        """
        try:
            locator = self.getLocatorsObject()
            search_box_path = self.findElementByXpath(xpath=locator.getInputSearchArea())
            search_box_path.send_keys(searchString + " wiki")
            search_button = self.findElementByXpath(xpath=locator.getSearchButton())
            search_button.submit()
            temp_a  = self.findElementByClass(locator.getSearchLinkClass())
            link = self.findElementByTag('a',temp_a)
            temp_b  =  link.get_attribute('href')
            if temp_b[25:29] != 'wiki':
                print("there is no wikipedia page associated with search string")
                return False
            else:
                link.click()
                return True
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(searchProduct) - Something went wrong on searching.\n" + str(e))

    def generateTitle(self, search_string):
        """
        This function generatesTitle for the products searched using search string
        :param search_string: product to be searched for.
        """
        try:
            title = search_string + "- Buy Products Online at Best Price in India - All Categories | Flipkart.com"
            return title
        except Exception as e:
            raise Exception(f"(generateTitle) - Something went wrong while generating complete title.\n" + str(e))

    def checkVisibilityOfElement(self, element_to_be_checked):
        """
        This function check the visibility of element on the webpage
        """
        try:
            if element_to_be_checked in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(checkVisibilityOfElement) - Not able to check for the element.\n" + str(e))


    def getProductSearched(self, search_string):
        """
        This function returns the name of product searched
        """
        try:
            return search_string
        except Exception as e:
            return search_string



    def wait(self):
        """
        This function waits for the given time
        """
        try:
            self.driver.implicitly_wait(2)
        except Exception as e:
            raise Exception(f"(wait) - Something went wrong.\n" + str(e))

    def generateDataForColumnAndFrame(self, response):
        """
        This function generates data for the column where only single data is presented. And then frames it in data frame.
        """
        try:
            data_frame1 = pd.DataFrame()
            flatten_rating = [j for i in response['ratings'] for j in i]
            for column_name, value in response.items():
                if column_name == 'product_searched' or column_name == 'product_name' or column_name == 'price' or column_name == 'discount_percent' or column_name == 'offer_details' or column_name == 'EMI':
                    list_value = []
                    for i in range(0, len(flatten_rating)):
                        list_value.append(response[column_name])
                    data_frame1.insert(0, column_name, list_value)
            print(data_frame1)
            return data_frame1
        except Exception as e:
            raise Exception(
                f"(dataGeneration) - Something went wrong on creating data frame and data for column.\n" + str(e))

    def frameToDataSet(self, response):
        """
        This function frames the column to dataframe.
        """
        try:
            data_frame2 = pd.DataFrame()
            for column_name, value in response.items():
                if column_name == 'product_searched' or column_name == 'product_name' or column_name == 'price' or column_name == 'discount_percent' or column_name == 'offer_details' or column_name == 'EMI':
                    continue
                else:
                    flatten_result = [values for lists in response[column_name] for values in lists]
                    data_frame2.insert(0, column_name, flatten_result)
            return data_frame2
        except Exception as e:
            raise Exception(
                f"(dataGeneration) - Something went wrong on creating data frame and data for column.\n" + str(e))

    def createDataFrameIncludingAllColumn(self, response):
        """
        This function creates dataframe from given data.
        """
        try:
            data_frame1 = self.generateDataForColumnAndFrame(response=response)
            data_frame2 = self.frameToDataSet(response=response)
            frame = [data_frame1, data_frame2]
            data_frame = pd.concat(frame, axis=1)
            return data_frame
        except Exception as e:
            raise Exception(f"(createDataFrame) - Something went wrong on creating data frame.\n" + str(e))

    def saveDataFrameToFile(self, dataframe, file_name):
        """
        This function saves dataframe into filename given
        """
        try:
            dataframe.to_csv(file_name)
        except Exception as e:
            raise Exception(f"(saveDataFrameToFile) - Unable to save data to the file.\n" + str(e))

    def closeConnection(self):
        """
        This function closes the connection
        """
        try:
            self.driver.close()
        except Exception as e:
            raise Exception(f"(closeConnection) - Something went wrong on closing connection.\n" + str(e))
    
    def getReference(self):
        try:
            locator = self.getLocatorsObject()
            ref_class1,ref_class2,ref_class3 = locator.getReferencesClass()
            selector_1 = locator.getCSSselector()
            Path1  =  self.findElementByClass(ref_class1)
            Ref_objects = self.findElementsByTag('li',Path1)
            Ref_list = []
            for i in Ref_objects:
                Ref_objects1 = self.findElementsByCSS(selector_1)
                for k in Ref_objects1:
                    ref_link = k.get_attribute('href')
                    Ref_list.append(ref_link)
            return Ref_list
        except Exception as e:
            try:
                Path1  =  self.findElementByClass(ref_class2)
                Ref_objects = self.findElementsByTag('li',Path1)
                Ref_list=[]
                for i in Ref_objects:
                    Ref_objects1 = self.findElementsByCSS(selector_1)
                    for k in Ref_objects1:
                        ref_link = k.get_attribute('href')
                        Ref_list.append(ref_link)
                return Ref_list
            except Exception as e:
                try:
                    Path1 = self.findElementByClass(ref_class3)
                    Ref_objects = self.findElementsByTag('li', Path1)
                    Ref_list = []
                    for i in Ref_objects:
                        Ref_objects1 = self.findElementsByCSS(selector_1,i)
                        for k in Ref_objects1:
                            ref_link = k.get_attribute('href')
                            Ref_list.append(ref_link)
                    return Ref_list
                except Exception as e:
                    raise Exception(f"(getReference) - Something went wrong on closing connection.\n" + str(e))
        
    def getSummarydetails(self,searchString):
        try:
            page =  wikipedia.page(searchString)
            page_title = page.title
            Summary = wikipedia.summary(searchString,sentences=5)
            return page_title,Summary
        except wikipedia.DisambiguationError as e:
            random_search_string = random.choice(e.options[0:3])
            page = wikipedia.page(random_search_string)
            page_title = page.title
            Summary = wikipedia.summary(random_search_string,sentences=5)
            return  page_title,Summary
        except Exception as e:
            raise Exception(f"(getSummarydetails) - Something went wrong on closing connection.\n" + str(e))

    def getallImages(self):
        try:
            image_drivers = self.findElementsBytag('img')
            image_url_list = set()
            if image_drivers != []:
                for i in image_drivers:
                    image_url_list.add(i.get_attribute('src'))
                image_list = []
                for temp_url in image_url_list:
                    img_url = urllib.request.urlretrieve(temp_url)
                    with open(img_url[0],"rb") as imageFile:
                        image_format = base64.b64encode(imageFile.read())
                        image_list.append(image_format)
            return image_list
        except Exception as e:
            raise Exception(f"(getallImages) - Something went wrong on closing connection.\n" + str(e))


    def getDetailsToDisplay(self, searchString, username, password,Summary):
        """
        This function returns the review and other detials of product
        """
        try:
            search = searchString
            mongoClient = MongoDBManagement(username=username, password=password)
            References = self.getReference()
            Images = self.getallImages()

            result = {'Search_name': search,
                      'Summary': Summary,
                      'References': References,
                      'Images':Images}
            mongoClient.insertRecord(db_name="Wiki-Summariser",
                                     collection_name=searchString,
                                     record=result)
            return search
        except Exception as e:
            self.closeConnection()
            raise Exception(f"(getDetailsToDisplay) - Something went wrong on yielding data.\n" + str(e))
