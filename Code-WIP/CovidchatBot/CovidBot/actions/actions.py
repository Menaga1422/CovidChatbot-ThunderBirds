import datetime as dt
from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from rasa_sdk.forms import FormAction


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")

        return []


class ActionDefineCovid(Action):

    def name(self) -> Text:
        return "action_define_covid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_text = tracker.latest_message['text']
        if "structure" in user_text:
            response = "SARS-CoV-2 is a single-stranded RNA-enveloped virus. An RNA-based metagenomic next-generation sequencing approach has been applied to characterize its entire genome, which is 29,881 bp in length, encoding 9860 amino acids. Gene fragments express structural and nonstructural proteins."

        elif ("full" in user_text or "expansion" in user_text or "stands for" in user_text):
            response = "'CO' stands for corona, 'VI' for virus, and 'D' for disease. Formerly, this disease was referred to as '2019 novel coronavirus' or '2019-nCoV.' The COVID-19 virus is a new virus linked to the same family of viruses as Severe Acute Respiratory Syndrome (SARS) and some types of common cold."
        else:
            response = "COVID-19 is the disease caused by a new coronavirus called SARS-CoV-2.WHO first learned of this new virus on 31 December 2019, following a report of a cluster of cases of ‘viral pneumonia’ in Wuhan, People’s Republic of China."
        dispatcher.utter_message(
            text=response, image="https://flowextra.com/public/images/news/1609397129Education%20sector%20bogged%20down%20by%20COVID-19%20lockdown,%20strikes%20in%202020.jpg")

        return []


class ActionDefineCovid(Action):

    def name(self) -> Text:
        return "action_show_covidstat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get(
            "https://data.covid19india.org/v4/min/data.min.json").json()
        print("json data", response)
        entities = tracker.latest_message["entities"]
        print("Message", entities)
        state = None

        for i in entities:
            if i['entity'] == "state":
                state = i['group']
            message = "Please check the spelling"

        for key, data in response.items():
            if key == state:
                message = "confirmed : " + str(data["total"]["confirmed"])+" \ndeceased" + str(data["total"]["deceased"]) +\
                    " recovered : " + str(data["total"]["recovered"]) +\
                    " tested : " + str(data["total"]["tested"]) +\
                    " vaccinated1 : " + str(data["total"]["vaccinated1"]) +\
                    " vaccinated2 : " + str(data["total"]["vaccinated2"])

        dispatcher.utter_message(text="Data", attachment=message)
        return []


class ActionCovidTest(Action):

    def name(self) -> Text:
        return "action_show_covidresult"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        results = ["Get a COVID-19 vaccine as soon as you can when eligible.\n\
        Individuals 12 years old and over are currently eligible.Stay home except to get medical care and take care of yourself. Call your medical provider if you start feeling worse.(not vaccinated)",
                   "Although the risk of being infected with the virus that causes COVID-19 is low if you are fully vaccinated, you should get tested and stay home and away from others. Talk to your healthcare provider for more information.\
        Contact your local emergency services for more information.\n",
                   "Based on the answers given, you do not need to get tested unless recommended or required by your healthcare provider, employer, or public health official."
                   ]
        if tracker.get_slot("is_vaccinated") == False:
            message = results[0]
        elif tracker.get_slot("is_sick") == True:
            message = results[1]
        else:
            message = results[2]
        dispatcher.utter_message(text=message)
        return []


class ActionSymptoms(Action):

    def name(self) -> Text:
        return "action_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_text = tracker.latest_message['text'].casefold()
        if "symptom" in user_text or "sign" in user_text or "feel" in user_text or "behave" in user_text or "happen" in user_text or "do" in user_text or "identify" in user_text or "affect" in user_text or "know" in user_text:
            response = "The most common symptoms of COVID-19 are fever, tiredness, and dry cough. Some patients may have aches and pains, nasal congestion, runny nose, sore throat or diarrhea. These symptoms are usually mild and begin gradually."

        elif ("die" in user_text):
            response = "Don't panic,stay home and get vaccinated as soon as possible.We will overcome this situation"

        elif ("cough" in user_text):
            response = "A cough is your body's way of responding when something irritates your throat or airways. An irritant stimulates nerves that send a message to your brain. The brain then tells muscles in your chest and abdomen to push air out of your lungs to force out the irritant. An occasional cough is normal and healthy."

        elif ("fever" in user_text):
            response = "A fever is a temporary increase in your body temperature, often due to an illness. Having a fever is a sign that something out of the ordinary is going on in your body."

        elif ("asymptomatic carrier" in user_text):
            response = "An asymptomatic carrier is a person or other organism that has become infected with a pathogen, but that displays no signs or symptoms"

        else:
            response = "COVID-19 is the disease caused by a new coronavirus called SARS-CoV-2.WHO first learned of this new virus on 31 December 2019, following a report of a cluster of cases of ‘viral pneumonia’ in Wuhan, People’s Republic of China."
        dispatcher.utter_message(text=response)

        return []


class ActionPrevention(Action):
    def name(self) -> Text:
        return "action_prevention"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_text = tracker.latest_message['text'].casefold()
        message="""Steps to follow every day:
	• Get a COVID-19 vaccine as soon as you can when eligible. Individuals 12 years old and over are currently eligible. Continue to follow the steps below every day until you are fully vaccinated.*
	• Wear a mask over your nose and mouth.*
	• Stay at least 6 feet away from people who don’t live with you.*
	• Avoid crowded areas and poorly ventilated spaces.*
	• Wash your hands often with soap and water, or use hand sanitizer with at least 60% alcohol."""

        if ("santitizer" in user_text):
            response = """Sanitizers are anti-microbial by their inherent chemical action. And they are effective in killing almost all microbes except 3 viruses (clostridium difficile, cryptosporum and noravirus.) 
Do not use hand-sanitizer if your hands are dirty and greasy. First clean your hands with soap and water and then use a sanitizer."""

        elif("when" in user_text or "long" in user_text or "often" in user_text):
            response = """Wash your hands for 20 seconds
After arriving.
After coughing or blowing your nose.
Before making or eating food.
After playing with animals.
After using the toilet.
After playing outdoors.
Before and after changing contact lenses."""

        elif "hand" in user_text or "soap" in user_text:
            response = "Regular handwashing is one of the best ways to remove germs, avoid getting sick, and prevent the spread of germs to others.Washing your hands with soap and water or using alcohol-based handrub kills viruses that may be on your hands."

        elif ("prevent" in user_text or "protect" in user_text or "safe" in user_text or "avoid" in user_text or "tips" in user_text or "reduce" in user_text):
            response = "Avoid touching surfaces, especially in public settings or health facilities, in case people infected with COVID-19 have touched them. Clean surfaces regularly with standard disinfectants"

        elif ("percent" in user_text or "%" in user_text or "amount" in user_text):
            response = "Alcohol-based hand sanitizers should contain at least 60% ethyl alcohol or isopropyl alcohol. These alcohols work to kill bacteria and viruses"

        else:
            response = "COVID-19 is the disease caused by a new coronavirus called SARS-CoV-2.WHO first learned of this new virus on 31 December 2019, following a report of a cluster of cases of ‘viral pneumonia’ in Wuhan, People’s Republic of China."
        dispatcher.utter_message(text=response,attachment=message)

        return []


class ActionCurve(Action):
    def name(self) -> Text:
        return "action_curve"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_text = tracker.latest_message['text'].casefold()

        if ("slow" in user_text or "reduce" in user_text or ("how" in user_text and "flatten" in user_text) or "prevent" in user_text):
            response = """when each person with the virus is infecting less than one new person on average — the virus will fade away.
 we can slow the spread of the virus by taking precautionary measures. By decreasing any part of the numbers that make up R0 — number of contacts, risk of transmission, or duration — we can decrease the number of new people contracting the virus, thus slowing the spread of disease"""

        elif("curve" in user_text):
            response = "The Nation preventing a health care system from being overwhelmed requires a society to do two things: 'flatten the curve'—that is, slow the rate of infection so there aren't too many cases that need hospitalization at one time—and 'raise the line'—that is, boost the hospital system's capacity to treat large numbers of patients."

        # elif("spike" in user_text) :
        #     response = "spikes are critically important. They are literally the point of contact that our own vulnerable lung cells have with the virus, SARS-CoV-2. Like a key cut for a specific lock, the spike slides neatly into the matching sites of receptors found on cells that line the airways of our lungs. Once secured, this connection allows the entire ball-shaped virus to slip into the cell. Inside, it makes thousands of copies of itself. And the potentially lethal infection has begun."

        elif ("fast" in user_text or "quick" in user_text or "transmit" in user_text or "spike" in user_text):
            response = """The virus can spread from an infected person’s mouth or nose in small liquid particles when they cough, sneeze, speak, sing or breathe. These particles range from larger respiratory droplets to smaller aerosols.
Current evidence suggests that the virus spreads mainly between people who are in close contact with each other, typically within 1 metre (short-range). A person can be infected when aerosols or droplets containing the virus are inhaled or come directly into contact with the eyes, nose, or mouth.
People may also become infected by touching surfaces that have been contaminated by the virus when touching their eyes, nose or mouth without cleaning their hands.
        4,771,343 people have died so far from the coronavirus COVID-19 outbreak as of
rowth factor is a quantity multiplies itself over time. The formula used is every day's new deaths / new deaths on the previous day. For example, a quantity growing by 7% every period (in this case daily) has a growth factor of 1.07.
A growth factor above 1 indicates an increase, whereas one between 0 and 1 it is a sign of decline, with the quantity eventually becoming zero.
A growth factor below 1 (or above 1 but trending downward) is a positive sign, whereas a growth factor constantly above 1 is the sign of exponential growth."""

        else:
            response = "COVID-19 is the disease caused by a new coronavirus called SARS-CoV-2.WHO first learned of this new virus on 31 December 2019, following a report of a cluster of cases of ‘viral pneumonia’ in Wuhan, People’s Republic of China."
        dispatcher.utter_message(text=response)

        return []




class ActionVaccine(Action):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    def name(self) -> Text:
        return "action_vaccine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message["entities"]
        for i in entities:
            if i['entity'] == "district":
                district = i['group']
            response = "Please check the spelling"

        # print(district)
        now = dt.datetime.now()
        date = now.strftime("%d-%m-%Y")
        # print("date"+date)

        URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}'.format(
            district, date)
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        counter = 0
        result = requests.get(URL, headers=header)
        response_json = result.json()
        data = response_json["sessions"]

        for each in data:
            if((each["available_capacity"] > 0) & (each["min_age_limit"] == 18)):
                counter += 1

                response = "Vaccine Center: " + str(each["name"])+'\n' +\
                    "Address: " + str(each["address"])+'\n' +\
                    "Pincode: " + str(each["pincode"])+'\n' +\
                    "Opening Time: " + str(each["from"])+'\n' +\
                    "Closing Time: " + str(each["to"])+'\n' +\
                    "Available Capacity: " + str(each["available_capacity"])+'\n' +\
                    "Available capacity dose1: " + str(each["available_capacity_dose1"])+'\n' +\
                    "Available capacity dose2: " + str(each["available_capacity_dose2"])+'\n' +\
                    "Fees: " + str(each["fee"])+'\n' +\
                    "Vaccine Name: " + str(each["vaccine"])+'\n' +\
                    "Slots: " + str(each["slots"])

        if(counter == 0):
            response = "No available slots"

        
        dispatcher.utter_message(text=response)
        return []
