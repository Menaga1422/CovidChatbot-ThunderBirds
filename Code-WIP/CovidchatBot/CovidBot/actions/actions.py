import datetime as dt
from logging import NullHandler
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

        elif ("full" in user_text or "expansion" in user_text or "stands for" in user_text or 'word' in user_text):
            response = "'CO' stands for corona, 'VI' for virus, and 'D' for disease. Formerly, this disease was referred to as '2019 novel coronavirus' or '2019-nCoV.' The COVID-19 virus is a new virus linked to the same family of viruses as Severe Acute Respiratory Syndrome (SARS) and some types of common cold."
        else:
            response = "COVID-19 is the disease caused by a new coronavirus called SARS-CoV-2.WHO first learned of this new virus on 31 December 2019, following a report of a cluster of cases of ‘viral pneumonia’ in Wuhan, People’s Republic of China."
        dispatcher.utter_message(
            text=response, image="https://www.fda.gov/files/Coronavirus_3D_illustration_by_CDC_1600x900.png")

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
        if entities == "none":
            message = "Give your state name"
        else:
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

        dispatcher.utter_message(text=message)
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
        message = """<b>Get a COVID-19 vaccine as soon as you can when eligible. Individuals 12 years old and over are currently eligible. </b>Continue to follow the steps below every day until you are fully vaccinated.
	<br>• Wear a <b>mask </b>over your nose and mouth.
	<br>• Stay at least<b> 6 feet </b>away from people who don’t live with you.
	<br>• Avoid crowded areas and poorly ventilated spaces.
	<br>• <b>Wash your hands</b> often with soap and water, or use hand sanitizer with at least 60% alcohol."""

        if ("santitizer" in user_text):
            response = """Sanitizers are anti-microbial by their inherent chemical action. And they are effective in killing almost all microbes.
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

        elif ("tips" in user_text or "contact" in user_text or "surface" in user_text):
            response = "Avoid touching surfaces, especially in public settings or health facilities, in case people infected with COVID-19 have touched them. Clean surfaces regularly with standard disinfectants"

        elif ("percent" in user_text or "%" in user_text or "amount" in user_text):
            response = "Alcohol-based hand sanitizers should contain at least 60% ethyl alcohol or isopropyl alcohol. These alcohols work to kill bacteria and viruses"

        else:
            response = message
        dispatcher.utter_message(text=response, attachment=message)

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
        district = "none"
        for i in entities:
            if i['entity'] == "district":
                district = i['group']
            response = "Please check the spelling"

        # print(district)
        now = dt.datetime.now()
        date = now.strftime("%d-%m-%Y")
        # print("date"+date)
        if(district == "none"):
            response = "Give your district name"
        else:
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

                    response = "<b>Vaccine Center:</b> " + str(each["name"])+'\n' +\
                        "<br><b>Address: </b>" + str(each["address"])+'\n' +\
                        "<br><b>Opening Time:</b> " + str(each["from"])+'\n' +\
                        "<br><b>Closing Time:</b> " + str(each["to"])+'\n' +\
                        "<br><b>Available Capacity:</b> " + str(each["available_capacity"])+'\n' +\
                        "<br><b>Available capacity dose1:</b> " + str(each["available_capacity_dose1"])+'\n' +\
                        "<br><b>Available capacity dose2:</b> " + str(each["available_capacity_dose2"])+'\n' +\
                        "<br>Fees: " + str(each["fee"])+'\n' +\
                        "<br>Vaccine Name: " + str(each["vaccine"])+'\n' +\
                        "<br>Slots: " + str(each["slots"])

            if(counter == 0):
                response = "No available slots"

        dispatcher.utter_message(text=response)
        return []


class ActionDistance(Action):

    def name(self) -> Text:
        return "action_distance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_text = tracker.latest_message['text']
        if "isolat" in user_text:
            response = "Isolation is used to separate people infected with COVID-19 from those who are not infected.People who are in isolation should stay home until it’s safe for them to be around others. At home, anyone sick or infected should separate from others, stay in a specific “sick room” or area, and use a separate bathroom."
        elif "quarantine" in user_text:
            response = "Quarantine if you have been in close contact with someone who has COVID-19, unless you have been fully vaccinated. People who are fully vaccinated do NOT need to quarantine after contact with someone who had COVID-19 unless they have symptoms. However, fully vaccinated people should get tested 3-5 days after their exposure, even if they don’t have symptoms and wear a mask indoors in public for 14 days following exposure or until their test result is negative.This will help to stop the spread over the country."
        elif "distance" in user_text or "length" in user_text or "gap" in user_text:
            response = "Social distancing is a non-pharmaceutical infection prevention and control intervention implemented to avoid/decrease contact between those who are infected with a disease causing pathogen and those who are not, so as to stop or slow down the rate and extent of disease transmission in a community.Ensure physical distancing of minimum 1metre."
        else:
            response = "To reduce the risk of getting affected by covid.Stay indoors and avoid outdoors."
        dispatcher.utter_message(text=response)

        return []


class ActionTest(Action):

    def name(self) -> Text:
        return "action_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_text = tracker.latest_message['text']
        response = '''1️⃣ Rapid diagnostic test (RDT) of a sample of the respiratory tract of a person helps to detect the viral proteins (antigens) related to COVID-19 virus. This ensures a speedy and accurate diagnosis and its usage is CDC-approved.
        <br>2️⃣ Polymerase chain reaction (PCR) tests are sent away to a lab to diagnose disease
        <br>3️⃣ Lateral flow tests (LFTs) can diagnose Covid-19 on the spot, but aren’t as accurate as PCR tests
        <br>4️⃣ Antibody (or serology) tests can’t diagnose active infection, but they can help to tell if a person has immunity to Covid-19
        '''
        dispatcher.utter_message(text=response)

        return []


class ActionTime(Action):

    def name(self) -> Text:
        return "action_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_text = tracker.latest_message['text']
        if "change" in user_text or 'mutate' in user_text:
            response = "Compared with HIV, SARS-CoV-2 is changing much more slowly as it spreads. But one mutation stood out to Korber. It was in the gene encoding the spike protein, which helps virus particles to penetrate cells. Korber saw the mutation appearing again and again in samples from people with COVID-19. At the 614th amino-acid position of the spike protein, the amino acid aspartate (D, in biochemical shorthand) was regularly being replaced by glycine (G) because of a copying fault that altered a single nucleotide in the virus’s 29,903-letter RNA code. Virologists were calling it the D614G mutation."
        elif "pandemic" in user_text:
            response = "The World Health Organization (WHO) on March 11, 2020, has declared the novel coronavirus (COVID-19) outbreak a global pandemic "
        elif "time" in user_text or "month" in user_text or "season" in user_text or "summer" in user_text or "winter" in user_text or "autumn" in user_text or "long" in user_text or "last" in user_text or "year" in user_text or "normal" in user_text or "away" in user_text or "over" in user_text or "end" in user_text:
            response = " Scientists think the virus that causes COVID-19 may be with us for decades or longer, but that doesn’t mean it will keep posing the same threat.The virus emerged in late 2019 and it’s difficult to predict how it will behave over the long term. But many experts believe it’s likely the disease will eventually ease from a crisis to a nuisance like the common cold."
        dispatcher.utter_message(text=response)

        return []


class ActionVulnerable(Action):

    def name(self) -> Text:
        return "action_vulnerable"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_text = tracker.latest_message['text']
        if ("children" in user_text or "baby" in user_text):
            response = "Children of all ages can become ill with coronavirus disease 2019. But most kids who are infected typically don't become as sick as adults and some might not show any symptoms at all."
        elif("pet" in user_text or "cat" in user_text or "dog" in user_text):
            response = "A small number of pets worldwide, including cats and dogs, have been reported to be infected with the virus that causes COVID-19, mostly after close contact with people with COVID-19."
        elif("pregnant" in user_text):
            response = "Pregnant women do not appear more likely to contract the infection than the general population. However, pregnancy itself alters the body’s immune system and response to viral infections in general, which can occasionally be related to more severe symptoms and this will be the same for COVID-19."
        elif("age" in user_text or "group" in user_text):
            response = " Population groups of 20-49 years of age and 50 years-above were highly vulnerable to infection. Interestingly, 20-49 years of age group was most affected in India. However, higher population of the deceased were reported in the 50 years-above in all countries."
        elif("aged" in user_text or "elder" in user_text or "parents" in user_text):
            response = "Although all age groups are at risk of contracting COVID-19, older people face significant risk of developing severe illness if they contract the disease due to physiological changes that come with ageing and potential underlying health conditions."
        elif("asthma" in user_text or "cancer" in user_text or "disease" in user_text):
            response = "Health conditions, such as heart or lung disease, can increase your risk of developing dangerous symptoms if you become infected with coronavirus disease 2019."
        elif("ventilator" in user_text or "severe" in user_text or "intense care" in user_text):
            response = "Ventilators can be lifesaving for people with severe respiratory symptoms. Roughly 2.5 percentTrusted Source of people with COVID-19 will need a mechanical ventilator."
        else:
            response = "People of all ages can be infected by the COVID-19 virus.Older people and younger people can be infected by the COVID-19 virus. Older people, and people with pre-existing medical conditions such as asthma, diabetes, and heart disease appear to be more vulnerable to becoming severely ill with the virus."

        dispatcher.utter_message(text=response)
        return []


class ActionOrigin(Action):

    def name(self) -> Text:
        return "action_origin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_text = tracker.latest_message['text']
        if("start" in user_text or "detect" in user_text or "come" in user_text):
            response = "The outbreak of Novel coronavirus disease (COVID-19) was initially noticed in a seafood market in Wuhan city in Hubei Province of China in mid- December, 2019, has now spread to 215 countries/territories/areas worldwide."
        else:
            response = "Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) is a novel severe acute respiratory syndrome coronavirus. It was first isolated from three people with pneumonia connected to the cluster of acute respiratory illness cases in Wuhan. All structural features of the novel SARS-CoV-2 virus particle occur in related coronaviruses in nature."

        dispatcher.utter_message(text=response)
        return []
