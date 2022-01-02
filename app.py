# doing necessary imports
import threading
from logger_class import getLog
from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin
import pandas as pd
from mongoDBOperations import MongoDBManagement
from WikiSummariser import WikiSummariser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

rows = {}
collection_name = None

logger = getLog('WikiSumm.py')

free_status = True
db_name = 'Wiki-Summariser'

app = Flask(__name__)  # initialising the flask app with the name 'app'

#For selenium driver implementation on heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")


#To avoid the time out issue on heroku
class threadClass:

    def __init__(self,searchString, wiki_object,Summary):
        self.searchString = searchString
        self.wiki_object = wiki_object
        self.Summary = Summary
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        global collection_name, free_status
        free_status = False
        collection_name = self.wiki_object.getDetailsToDisplay(searchString=self.searchString, username='Akhi_01',
                                                                   password='Akhanu',Summary=self.Summary)
        print("Akhi_dbg2:"+collection_name)
        logger.info("Thread run completed")
        free_status = True


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        global free_status
        ## To maintain the internal server issue on heroku
        if free_status != True:
            return "This website is executing some process. Kindly try after some time..."
        else:
            free_status = True
        searchString = request.form['content']# obtaining the search string entered in the form
        #expected_review = int(request.form['expected_review'])
        try:
            wiki_object = WikiSummariser(executable_path=ChromeDriverManager().install(),
                                               chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='mongodb', password='mongodb')
            wiki_object.openUrl("https://www.google.com/")
            logger.info("Url hitted")
            searchString,Summary = wiki_object.getSummarydetails(searchString)
            wiki_object.searchProduct(searchString=searchString)
            logger.info(f"Search begins for {searchString}")
            if mongoClient.isCollectionPresent(collection_name=searchString, db_name=db_name):
                response = mongoClient.findAllRecords(db_name=db_name, collection_name=searchString)
                summary = response[0]
                wiki_object.saveDataFrameToFile(file_name="static/summary_data.csv",
                                                        dataframe=pd.DataFrame(summary))
                logger.info("Data saved in scrapper file")
                return render_template('results.html', rows=summary)  # show the results to user
            else:
                threadClass(searchString=searchString,wiki_object=wiki_object,Summary=Summary)
                return redirect(url_for('feedback'))

        except Exception as e:
            raise Exception("(app.py) - Something went wrong while rendering all the details of product.\n" + str(e))

    else:
        return render_template('index.html')


@app.route('/feedback', methods=['GET'])
@cross_origin()
def feedback():
    try:
        global collection_name
        print(collection_name)
        if collection_name is not None:
            wiki_object = WikiSummariser(executable_path=ChromeDriverManager().install(),
                                               chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='mongodb', password='mongodb')
            rows = mongoClient.findAllRecords(db_name="Wiki-Summariser", collection_name=collection_name)
            summary = rows[0]
            dataframe = pd.DataFrame(summary)
            wiki_object.saveDataFrameToFile(file_name="static/summary_data.csv", dataframe=dataframe)
            collection_name = None
            return render_template('results.html', rows=summary)
        else:
            return render_template('results.html', rows=None)
    except Exception as e:
        raise Exception("(feedback) - Something went wrong on retrieving feedback.\n" + str(e))

if __name__ == "__main__":
    app.run()  # running the app on the local machine on port 8000
