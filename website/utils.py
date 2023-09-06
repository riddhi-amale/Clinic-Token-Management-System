from pymongo import MongoClient, collation
import os
from datetime import datetime, timedelta
from fpdf import FPDF

def connect_mongodb(database, collection):
    client=MongoClient("mongodb+srv://shahclinicpune:sandeepshah@appointments-cluster.bgggw.mongodb.net/morning?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    db=client[database]
    coll=db[collection]
    return coll

def get_current_token(slot):
    coll=connect_mongodb(slot,"tokens")
    document=coll.find_one({"t_name":"current_token_today"})
    return document["t_number"]

def get_assign_token(date, time):
    coll=connect_mongodb(time,"tokens")
    document=coll.find_one({"t_name":"assign_token_"+date})
    return document["t_number"]

def increment_token(date,time,token_name):
    coll=connect_mongodb(time,"tokens")
    number=coll.find_one({"t_name":token_name+date})["t_number"]
    coll.update_one({"t_name":token_name+date},{"$set":{"t_number":number+1}})

def check_slot():
    current_hour = datetime.now().hour
    if current_hour >= 10 and current_hour <= 13:
        return "morning"
    if current_hour >= 17 and current_hour <= 20:
        return "evening"
    return "invalid"

def check_phone_number(phone_number):
    coll=connect_mongodb("morning","patients")
    db_phone_numbers = [x["p_number"] for x in coll.find()]
    coll=connect_mongodb("evening","patients")
    db_phone_numbers += [x["p_number"] for x in coll.find()]
    return phone_number in db_phone_numbers
    
def add_patient(p_name, p_number, my_token, date,time):
    coll=connect_mongodb(time,"patients")
    today_date = datetime.now()
    tomorrow_date = today_date + timedelta(1)
    today_date = today_date.strftime('%d-%m-%Y')
    tomorrow_date = tomorrow_date.strftime('%d-%m-%Y')
    if date == "today":
        coll.insert_one({"p_name":p_name,"p_number":p_number,"date":today_date,"t_number":my_token})
        return today_date
    else:
        coll.insert_one({"p_name":p_name,"p_number":p_number,"date":tomorrow_date,"t_number":my_token})
        return tomorrow_date

def get_patients(time):
    today_date = datetime.now()
    tomorrow_date = today_date + timedelta(1)
    today_date = today_date.strftime('%d-%m-%Y')
    tomorrow_date = tomorrow_date.strftime('%d-%m-%Y')
    coll=connect_mongodb(time,"patients")
    today_patients=[]
    tomorrow_patients=[]
    for document in coll.find():
        if document["date"] == today_date:
            today_patients.append(list(document.items())[1:])
        else:
            tomorrow_patients.append(list(document.items())[1:])
    return today_patients,tomorrow_patients

def clear_patients():
    coll=connect_mongodb("morning","patients")
    coll.delete_many({})
    coll=connect_mongodb("evening","patients")
    coll.delete_many({})

def reset_tokens(date,time):
    coll=connect_mongodb(time,"tokens")
    coll.update_one({"t_name":"current_token_"+date},{"$set":{"t_number":0}})
    coll.update_one({"t_name":"assign_token_"+date},{"$set":{"t_number":1}})

def slot_availability():
    pref_coll=connect_mongodb("preferences","max_patients")
    max_tokens_list =[list(document.values())[1] for document in pref_coll.find()]
    assign_tokens_list = []
    morning_coll=connect_mongodb("morning","tokens")
    evening_coll=connect_mongodb("evening","tokens")
    assign_tokens_list.append(morning_coll.find_one({"t_name":"assign_token_today"})["t_number"])
    assign_tokens_list.append(evening_coll.find_one({"t_name":"assign_token_today"})["t_number"])
    assign_tokens_list.append(morning_coll.find_one({"t_name":"assign_token_tomorrow"})["t_number"])
    assign_tokens_list.append(evening_coll.find_one({"t_name":"assign_token_tomorrow"})["t_number"])

    current_hour = datetime.now().hour
    today_date = datetime.now()
    tomorrow_date = today_date + timedelta(1)
    today_date = today_date.strftime('%d-%m-%Y')
    tomorrow_date = tomorrow_date.strftime('%d-%m-%Y')
    morning_time=" [10:00am - 01:00pm]"
    evening_time=" [05:00pm - 08:00pm]"
    choices=[]
    j=0
    for i,assign_token, max_token in zip(range(4),assign_tokens_list,max_tokens_list):
        if assign_token <= max_token:
            if i == 0 and current_hour<=13:
                choices.append((j,str(today_date)+str(morning_time)))
                j+=1
            elif i == 1 and current_hour<=20:
                choices.append((j,str(today_date)+str(evening_time)))
                j+=1
            elif i == 2:
                choices.append((j,str(tomorrow_date)+str(morning_time)))
                j+=1
            elif i == 3:
                choices.append((j,str(tomorrow_date)+str(evening_time)))
                j+=1
    return choices

def get_slot_from_form(selected_choice):
    today_date = datetime.now().strftime('%d-%m-%Y')
    if today_date in selected_choice:
        if "10:00am" in selected_choice:
            return "today","morning"
        else:
            return "today","evening"

    else:
        if "10:00am" in selected_choice:
            return "tomorrow","morning"
        else:
            return "tomorrow","evening"


    

