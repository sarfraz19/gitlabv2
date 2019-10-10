import urllib3, json, array, csv, os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd

http = urllib3.PoolManager()

project_key = input("enter the project key :")

datevalue = datetime.strftime(datetime.now() - timedelta(10), '%Y-%m-%d')

print(datevalue)
with open('#repository.csv','rt') as f:
    data = csv.reader(f)
    for row in data:
        url = "https://gitlab.com/api/v4/projects/"+str(row[1])+"/repository/branches"
        response = http.request('GET', url , headers={"PRIVATE-TOKEN" : project_key})
        print("==============")
        print(str(row[0]))
        if response.status == 200:
            print("status: success")
        else:
            print("  status: Failure")
        print("==============")
        #========data===========
        soup = BeautifulSoup(response.data, "html.parser")
        #========json_data===========
        json_data = json.loads(soup.text)
        #========indi_json_data===========
        for i in json_data:
            print("->"+str(i['name']))
            if response.status == 200:
                print("  status: success")
            else:
                print("  status: Failure")
            url = "https://gitlab.com/api/v4/projects/"+str(row[1])+"/repository/commits?ref_name="+str(i['name'])+"&per_page=10000&since="+datevalue
            response = http.request('GET', url , headers={"PRIVATE-TOKEN" : project_key})
            soup = BeautifulSoup(response.data, "html.parser")
            json_data = json.loads(soup.text)
            #
            #specify the path here
            #
            path = os.getcwd()+'\\#result\\'
            try:
                pd.read_json(json.dumps(json_data)).to_csv(path+str(row[0])+'_'+str(i['name'])+'.csv', columns=['id',  'title',  'committer_name', 'committer_email', 'committed_date'])
            except:
                print(" ")
                if str(i):
                    print(str(i)+" has no commits")             
                print(" ")


