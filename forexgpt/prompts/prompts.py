import json
import config as _conf
from metalpriceapi.client import Client

def get_live_gold_price():
    metal_api_client = Client(_conf.METALAPI_API_KEY)

    gold_response=metal_api_client.fetchLive(base='USD', currencies=['XAU'])

    if gold_response["success"]==True:
        return round(1/float(gold_response["rates"]["XAU"]),2)
    
    else:
        return "there was an error making the api call"

class Prompt:
    def __init__(self) -> None:
        self.base_prompt = {
                "prompt_name": "base_prompt",
                "prompt": f'''You are a forex trading coach. You focus on trading Gold and your main method is price action. You accept either text questions, screenshots to analyze, or both.

                            Your name is Forex Anne.

                            Please exclude fibonacci, candle engulfing, trendlines, and indicators in your analysis and focus on price action, first touch, and second touch (support and resistance).

                            The Analysis must be based on Scalping Type Trading (Scalpers), unless it is based on Bigger Time Frame and Bigger Price Action.
                            
                            Provide information relating it with Fundamental Analysis only when asked or needed in the particular situation.

                            Please keep your replies concise and limit it to 1000 characters.

                            Always base your recommendations on the current price of gold which is {get_live_gold_price()}
                            \n 
                        '''
                        # Based on the above, please respond to the following:
                        }
        self.journal_prompt = {
            "prompt_name": "journal_prompt",
            "prompt": ''' You are a forex journal assisstant. You focus on Gold and your main method is price action. When a student sends you a trade screenshot,
                            you help them create a brief journal entry that includes the price, the support and resistance levels, and the profit and/or losses if any.
                            Please keep your replies concise and limit it to 1000 characters.
                        '''
        }

    def return_base_prompt(self):
        return self.base_prompt["prompt"]
    
    def save_base_prompt_to_json(self):
        with open('forexgpt/base-prompt.json', 'w', encoding='utf-8') as f:
            json.dump(self.base_prompt,f)
    
    def return_journal_prompt(self):
        return self.journal_prompt["prompt"]
    
    def save_journal_prompt_to_json(self):
        with open('forexgpt/journal-prompt.json', 'w', encoding='utf-8') as f:
            json.dump(self.journal_prompt,f)
    
# Prompt().save_base_prompt_to_json()
# print(Prompt().return_base_prompt())

# Prompt().save_journal_prompt_to_json()
# print(Prompt().return_journal_prompt())

# correct_id=1202078107046264884
# incorrect_id=1202078107046264883

# exists = any(d['value'] == incorrect_id for d in channel_ids if 'value' in d)
# print(exists)

            
