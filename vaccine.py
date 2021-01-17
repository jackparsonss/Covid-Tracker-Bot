import requests
from requests_html import HTML

class Vaccine:
    humans_vaccinated_url = 'https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/vaccinations.csv'
    r_html = None
    last_indexes = [19, 32, 57, 75, 94, 128, 150, 180, 203, 220, 230, 240, 260, 287, 308, 324, 337, 357, 360, 380, 381, 401, 402, 404, 418, 447, 468, 469, 489, 512, 528, 547, 571, 581, 615, 634, 652, 671, 690, 710, 740, 746, 780, 787, 789, 802, 815, 827, 842, 843, 848, 860, 887, 914, 948, 982]
    
    def __init__(self):
        self.r_html = self.get_html_data()
        self.last_index = 2

    def get_html_data(self):
        # return html file which can be searched using 'find' method
        r = requests.get(self.humans_vaccinated_url)
        if r.status_code != 200:
            print('failed to load html data')
        r_html = HTML(html = r.text)
        return r_html
    
    def get_element(self,id_name):
        return self.r_html.find(id_name)

    def get_element_component(self,element,comp_name):
        return element.find(comp_name)

    def get_headings(self):
        top_row = self.get_element('#LC1')
        return self.get_element_component(top_row[0],'th')[0:8]

    def get_row_data(self,index):
        row = self.get_element('#LC'+str(index))
        if len(row) != 0:
            return self.get_element_component(row[0],'td')[1:9]
        return []

    def update_last_indexes(self):
        self.last_indexes = []
        is_not_latest = True
        i = 0 
        while is_not_latest:
                if len(self.get_row_data(self.last_index+1)) != 0:
                    if self.get_row_data(self.last_index)[1].text == self.get_row_data(self.last_index+1)[1].text:
                        self.last_index +=1
                    else:
                        self.last_indexes.append(self.last_index)
                        self.last_index +=1
                else:
                    self.last_indexes.append(self.last_index)
                    is_not_latest = False
                i +=1
        return True

    def two_dim_grid(self):
        two_dim_grid=[]
        for index in self.last_indexes:
            row_data = self.get_row_data(index)
            rr=[]
            for item in self.get_row_data(index):
                rr.append(item.text)
            two_dim_grid.append(rr)
        return two_dim_grid
    
    def data(self):
        big_set = []
        two_dim_grid = self.two_dim_grid()
        for i in range(len(two_dim_grid)):
            temp_dic ={}
            headings = self.get_headings()
            for j in range(len(headings)):
                temp_dic[headings[j].text] = two_dim_grid[i][j]
            big_set.append(temp_dic)
        return big_set

    def find_dict_by_name(self,name_given):
        vaccine_data = self.data()
        for i in range(len(vaccine_data)):
            if vaccine_data[i].get('location') == name_given.title():
                return vaccine_data[i]

    def get_total_vaccinations(self,this_country):
        given_dict = self.find_dict_by_name(this_country)
        return given_dict['total_vaccinations'] if given_dict else None

    def get_people_vaccinated(self,this_country):
        given_dict = self.find_dict_by_name(this_country)
        return given_dict['people_vaccinated'] if given_dict else None
    
    def get_daily_vaccinations(self,this_country):
        given_dict = self.find_dict_by_name(this_country)
        return given_dict['daily_vaccinations'] if given_dict else None


#vaccine = Vaccine()
# --------------------------------------------
#                  WARNING(time cosuming only uncomment when you want to update to latest data example once a day)
# vaccine.update_last_indexes()
#--------------------------------------------

#country_name = input("Give a country name: ")
#print(vaccine.get_people_vaccinated('Canada'))
#print(vaccine.get_daily_vaccinations(country_name))
#print(vaccine.get_total_vaccinations(country_name))
