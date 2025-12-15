from word2number import w2n


class NumberPeopleClass:

    def __init__(self, tracker, personList):
        self.ROI1 = "bar"
        self.ROI2 = "unisa store"
        self._number_entities = 0
        self._sentence = "people"
        self._tracker = tracker
        self._message = tracker.latest_message["text"]
        self._entities = tracker.latest_message["entities"]
        self._location_1 = {"is_set":False, "place":None, "comparison_sign":None, "number":None, "name_slot":None, "negation": False}
        self._location_2 = {"is_set":False, "place":None, "comparison_sign":None, "number":None, "name_slot":None, "negation": False}
        self._name_entities = {}
        self._person_list = personList
        self._assegnation_values()
        self._assegnation_values_to_locations()
        
        

    def get_sentece(self):
        return "There are " + str(len(self._person_list)) + " " + self._sentence


    def _add_to_sentence(self, string, location=False):
        if not location:
            word = string
            if word.startswith("not_"):
                word = word[len("not_"):]
            if word == string:
                string = "are wearing " + word
            else:
                string = "aren't wearing " + word
        if self._number_entities == 0:
            self._sentence = self._sentence + " " + string
            self._number_entities = 1
        else:
            self._sentence = self._sentence + " and " + string

    def _assegnation_values(self):
        gender = self._tracker.get_slot("gender")
        if gender != None:
            if gender == "True":
                self._name_entities["gender"] = "male"
                self._sentence = self._sentence.replace("people", "male")
            else:
                self._name_entities["gender"] = "female"
                self._sentence = self._sentence.replace("people", "female")

        upper_color = self._tracker.get_slot("upper_color")
        if upper_color != None:
            self._name_entities["upper_color"] = upper_color
            self._add_to_sentence(upper_color + " shirts")

        lower_color = self._tracker.get_slot("lower_color")
        if lower_color != None:
            self._name_entities["lower_color"] = lower_color
            self._add_to_sentence(lower_color + " jeans")

        bag_presence = self._tracker.get_slot("bag_presence")
        if bag_presence != None:
            self._name_entities["bag"] = (bag_presence == "True" or bag_presence == True or bag_presence == "true")
            if self._name_entities["bag"]:
                self._add_to_sentence("bag")
            else:
                self._add_to_sentence("not_bag")

        hat_presence = self._tracker.get_slot("hat_presence")
        if hat_presence != None:
            self._name_entities["hat"] = ((hat_presence == "True") or (hat_presence == True) or (hat_presence == "true"))
            if self._name_entities["hat"]:
                self._add_to_sentence("hat")
            else:
                self._add_to_sentence("not_hat")

    def _assegnation_values_to_locations(self):
        # start_location_1 = -1
        # start_location_2 = -1
        sentence1 = ""
        sentence2 = ""
        negation = False
        for e in self._entities:
            entity = e["entity"]
            if entity == "negation":
                negation = True
            elif entity != "location":
                negation = False
                # index = self._entities.index(entity)
                # if self._entities[index+1] == "location":
                #     if not self._location_1["is_set"]:
                #         self._location_1["negation"] = True
                #     else:
                #         self._location_2["negation"] = True
            if entity == "location":
                if not self._location_1["is_set"]:
                    if e["value"] == self.ROI1:
                        self._location_1["place"] = "roi1"
                        sentence1 = sentence1 + " present in " + self.ROI1
                    elif e["value"] == self.ROI2:
                        self._location_1["place"] = "roi2"
                        sentence1 = sentence1 + " present in " + self.ROI2
                    
                    if negation:
                        self._location_1["negation"] = negation
                        negation = False
                        sentence1 = "not " + sentence1
                    self._location_1["is_set"] = True
                    self._location_1["name_slot"]="passages"
                    #start_location_1 = e["start"]
                else:
                    if e["value"] == self.ROI1:
                        self._location_2["place"] = "roi1"
                        sentence2 = sentence2 + " present in " + self.ROI1
                    else:
                        self._location_2["place"] = "roi2"
                        sentence2 = sentence2 + " present in " + self.ROI2
                    if negation:
                        self._location_2["negation"] = negation
                        negation = False
                        sentence2 = "not " + sentence2
                    self._location_2["is_set"] = True
                    self._location_2["name_slot"]="passages"
                    #start_location_2 = e["start"]
            
            elif entity == "comparison_sign":
                if self._location_1["comparison_sign"] == None:
                    self._location_1["comparison_sign"] = e["value"]
                    sentence1 = sentence1 + " " + e["value"] + " than"
                else:
                    self._location_2["comparison_sign"] = e["value"]
                    sentence2 = sentence2 + " " + e["value"] + " than"
                    

            elif entity == "number":
                if self._location_1["number"] == None:
                    self._location_1["number"] = w2n.word_to_num(e["value"])
                    sentence1 = sentence1 + " " + e["value"]
                    try:
                        if self._message[e['end']+1:e['end']+7] == "minute":
                            self._location_1["name_slot"]="persistence_time"
                            sentence1 = sentence1 + " minutes"
                        else:
                            sentence1 = sentence1 + " times"
                    except:
                        pass
                else:
                    self._location_2["number"] = w2n.word_to_num(e["value"])
                    sentence2 = sentence2 + " " + e["value"]
                    try:
                        if self._message[e['end']+1:e['end']+7] == "minute":
                            self._location_2["name_slot"]="persistence_time"
                            sentence2 = sentence2 + " minutes"
                        else:
                            sentence2 = sentence2 + " times"
                    except:
                        pass
        if sentence1 != "":
            self._add_to_sentence(sentence1, True)
            if sentence2 != "":
                self._add_to_sentence(sentence2, True)

    def print_entities(self):
        print(self._entities)
        print("Message: " + self._message)
        print("Entities:")


        for k in self._name_entities.keys():
            print(k + ": " + str(self._name_entities[k]))
        if self._location_1["is_set"]:
            if self._location_1["comparison_sign"] != None:
                print(self._location_1["name_slot"] + ":", self._location_1["comparison_sign"], "than", self._location_1["number"], "in", self._location_1["place"])
            else:
                print(self._location_1["place"] + ":", (not self._location_1["negation"]))
        if self._location_2["is_set"]:
            if self._location_2["comparison_sign"] != None:
                print(self._location_2["name_slot"] + ":", self._location_2["comparison_sign"], "than", self._location_2["number"], "in", self._location_2["place"])
            else:
                print(self._location_2["place"] + ":", (not self._location_2["negation"]))
        print("\n")



    def find_people(self):
        for e in self._name_entities.keys():
            
            value = self._name_entities[e]
            negation = False
            try:
                if value[0:4] == "not_":
                    negation = True
                    value = value[len("not_"):]
            except:
                pass
            self._delete_persons(e, value, negation)
        if self._location_1["is_set"]:
            self._delete_persons_without_locations(self._location_1)
        if self._location_2["is_set"]:
            self._delete_persons_without_locations(self._location_2)
        return "There are " + str(len(self._person_list)) + " people."

    def _delete_persons(self, slot, value, negation):
        """Delete people that have a a value in the slot different from the value passed as input"""
        for p in self._person_list.copy():
            if negation ^ (p[slot] != value):
                self._person_list.remove(p)

    def _delete_persons_without_locations(self, location):
            if location["comparison_sign"] == None:
                # not negation è stato inserito perchè il  metodo _delete_persons elimina tutte le persone che hanno un valore nello slot
                # diverso da quello passato in input.
                # In questo caso, se non metto la negazione (quindi negation è false), voglio eliminare tutte le persone che in
                # roi#_passages hanno un valore uguale a 0, per questo deve essere True il negation che passo al metodo _delete_persons.
                # In caso ontrario, cioè se negation è True, voglio trovare tutte le persone che non si trovano in roi#.
                # Quindi devo eliminare le persone che hanno un valore diverso a 0. In questo caso, il negation che dovrò passara
                # al metodo _delete_persons deve essere False.
                self._delete_persons(location["place"]+"_passages", 0, (not location["negation"]))
            elif location["comparison_sign"] == "greater":
                self._delete_lesser(location)
            else:
                self._delete_greater(location)

    def _delete_lesser(self, location):
        name_slot = location["place"] + "_" + location["name_slot"]
        for p in self._person_list.copy():
            if (p[name_slot] < location["number"]) or p[name_slot] == 0:
                self._person_list.remove(p)

    def _delete_greater(self, location):
        name_slot = location["place"] + "_" + location["name_slot"]
        for p in self._person_list.copy():
            if (p[name_slot] >= location["number"])  or p[name_slot] == 0:
                self._person_list.remove(p)






# class NumberPeopleClass:

#     def __init__(self, tracker, personList):
#         self.ROI1 = "bar"
#         self.ROI2 = "unisa store"

#         self._tracker = tracker
#         self._message = tracker.latest_message["text"]
#         self._entities = tracker.latest_message["entities"]
#         self._location_1 = {"is_set":False, "place":None, "comparison_sign":None, "number":None, "name_slot":None}
#         self._location_2 = {"is_set":False, "place":None, "comparison_sign":None, "number":None, "name_slot":None}
#         self._slot_1 = {"is_set":False, "name_slot":None, "value":None, "negation":False}
#         self._slot_2 = {"is_set":False, "name_slot":None, "value":None, "negation":False}
#         self._name_entities = []
#         self._person_list = personList

#         self._assegnation_name_entities()

#         for i in range(0, len(self._name_entities)):
#             if (self._name_entities[i] != "negation") and (not self._slot_1["is_set"]):
#                 self._slot_1 = self._assegnation_values(i)
                
#             elif self._name_entities[i] != "negation":
#                 self._slot_2 = self._assegnation_values(i)


#     def _assegnation_name_entities(self):
#         for e in self._entities:
#             entity = e["entity"]
#             if entity == "location":
#                 place = None
#                 if e["value"] == self.ROI1:
#                     place = "roi1"
#                 else:
#                     place = "roi2"
#                 if not self._location_1["is_set"]:
#                     self._location_1["is_set"] = True
#                     self._location_1["place"] = place
#                 else:
#                     self._location_2["is_set"] = True
#                     self._location_2["place"] = place
                    
#             elif entity == "comparison_sign":
#                 if self._location_1["comparison_sign"] == None:
#                     self._location_1["comparison_sign"] = e["value"]
#                 else:
#                     self._location_2["comparison_sign"] = e["value"]

#             elif entity == "number":
#                 if self._location_1["number"] == None:
#                     self._location_1["number"] = w2n.word_to_num(e["value"])
#                     try:
#                         if self._message[e['end']+1:e['end']+7] == "minute":
#                             self._location_1["name_slot"]="persistence_time"
#                         else:
#                             self._location_1["name_slot"]="passages"
#                     except:
#                         self._location_1["name_slot"]="passages"
#                 else:
#                     self._location_2["number"] = w2n.word_to_num(e["value"])
#                     try:
#                         if self._message[e['end']+1:e['end']+7] == "minute":
#                             self._location_2["name_slot"]="persistence_time"
#                         else:
#                             self._location_2["name_slot"]="passages"
#                     except:
#                         self._location_1["name_slot"]="passages"

#             # elif entity != "upper_cloth" and entity != "lower_cloth":
#             #     self._name_entities.append(entity)
#             elif entity == "upper_cloth"



#     def _assegnation_values(self, i):
#         slot = {"is_set":False, "name_slot":None, "value":None, "negation":False}
#         slot["name_slot"] = self._name_entities[i]
#         entity = slot["name_slot"]
#         if entity == "bag_presence" or entity == "hat_presence":
#             slot["value"] = self._tracker.get_slot(entity) == "True"
#             slot["name_slot"] = entity.removesuffix("_presence")
#         elif entity == "gender":
#             if self._tracker.get_slot(entity) == "True":
#                 slot["value"] = "male"
#             else:
#                 slot["value"] = "female"
#         else:
#             slot["value"] = self._tracker.get_slot(entity)
#         if i!=0 and self._name_entities[i-1] == "negation":
#             slot["negation"] = True
#         slot["is_set"] = True
#         return slot


#     def print_entities(self):
#         print("Message: " + self._message)
#         print("Entities:")
#         if self._slot_1["is_set"]:
#             if not self._slot_1["negation"]:
#                 print(self._slot_1["name_slot"] + ":", self._slot_1["value"])
#             else:
#                 print(self._slot_1["name_slot"] + ": not", self._slot_1["value"])
#         if self._slot_2["is_set"]:
#             if not self._slot_2["negation"]:
#                 print(self._slot_2["name_slot"] + ":", self._slot_2["value"])
#             else:
#                 print(self._slot_2["name_slot"] + ": not", self._slot_2["value"])
#         if self._location_1["is_set"]:
#                 print(self._location_1["name_slot"] + ":", self._location_1["comparison_sign"], "than", self._location_1["number"], "in", self._location_1["place"])
#         if self._location_2["is_set"]:
#                 print(self._location_2["name_slot"] + ":", self._location_2["comparison_sign"], "than", self._location_2["number"], "in", self._location_2["place"])
#         print("\n")


#     def find_persons(self):
#         if self._slot_1["is_set"]:
#             self._delete_persons(self._slot_1)
#         if self._slot_2["is_set"]:
#             self._delete_persons(self._slot_2)
#         if self._location_1["is_set"]:
#             self._delete_persons_without_locations(self._location_1)
#         if self._location_2["is_set"]:
#             self._delete_persons_without_locations(self._location_2)
#         return "There are " + str(len(self._person_list)) + " people."

#     def _delete_persons(self, slot):
#         for p in self._person_list.copy():
#             if slot["negation"] ^ (p[slot["name_slot"]] != slot["value"]):
#                 self._person_list.remove(p)

#     def _delete_persons_without_locations(self, location):
#             if location["comparison_sign"] == "greater":
#                 self._delete_greater(location)
#             else:
#                 self._delete_lesser(location)

#     def _delete_greater(self, location):
#         name_slot = location["place"] + "_" + location["name_slot"]
#         for p in self._person_list.copy():
#             if (p[name_slot] < location["number"]) or p[name_slot] == 0:
#                 self._person_list.remove(p)

#     def _delete_lesser(self, location):
#         name_slot = location["place"] + "_" + location["name_slot"]
#         for p in self._person_list.copy():
#             if (p[name_slot] >= location["number"])  or p[name_slot] == 0:
#                 self._person_list.remove(p)