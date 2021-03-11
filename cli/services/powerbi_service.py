import requests
from requests import HTTPError
import json
from datetime import datetime

class PowerBIService:
    def __init__(self, api_url):
        self.api_url = api_url        

    def push_data(self, product, version, release_date, lead_time_for_changes, deploy_freq, deploy_freq_date):
        payload = self.prepare_payload(product, version, release_date, lead_time_for_changes, deploy_freq, deploy_freq_date)   
        self.push_to_pbi(payload)
    
    def push_data_all(self, product, leadtimes_all, deploy_freq_per_release):        
        
        for key in leadtimes_all:
            l = leadtimes_all[key]
            if "lead-time" in l:
                payload = self.prepare_payload(product=product, 
                version=key, 
                release_date=l["release-date"], 
                lead_time_for_changes=l["lead-time"],
                deploy_freq=deploy_freq_per_release[key]["deploy_freq"],
                deploy_freq_date=deploy_freq_per_release[key]["releaseDate"])
            else:
                payload = self.prepare_payload(product=product, 
                version=key, 
                release_date=l["release-date"],                 
                deploy_freq=deploy_freq_per_release[key]["deploy_freq"],
                deploy_freq_date=deploy_freq_per_release[key]["releaseDate"])

            self.push_to_pbi(payload)

    def prepare_payload(self, product, version="N/A", release_date="1969/01/01", story_points=0, lead_time_for_changes="-1", deploy_freq="-1", deploy_freq_date=datetime.today()):
        payload_json =[{
            "product": product,
            "version": version,
            "release-date": release_date,
            "leadtimeforchanges": lead_time_for_changes,
            "deploy-freq":deploy_freq,
            "deploy-freq-date": deploy_freq_date
        }]
                
        return json.dumps(payload_json)
        
    def push_deploy_freq(self, product, deploy_freq, deploy_freq_date):
        payload = self.prepare_payload(product=product, deploy_freq=deploy_freq, deploy_freq_date=deploy_freq_date)
        self.push_to_pbi(payload)

    def push_to_pbi(self, payload):
        try:            
            url = self.api_url
            querystring = {}        
            headers = {'Content-Type': 'application/json'}

            response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
            print("INFO: Data pushed to PowerBI")
        except HTTPError:
            sys.exit("ERROR: The was an issue with the api url provided or the data provided.")