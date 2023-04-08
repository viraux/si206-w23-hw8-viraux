# Your name: AJ deVaux
# Your student id: 6472 4356
# Your email: ajdv@umich.edu
# List who you have worked with on this homework:
import matplotlib
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    d = {}
    data = cur.execute("SELECT * FROM restaurants").fetchall()
    for place in data:
        name = place[1]
        type = cur.execute("""SELECT Categories.category FROM Categories JOIN restaurants
        ON Categories.id = (?)""",(place[-3],)).fetchone()[0]
        # print(type)
        location = cur.execute("""SELECT Buildings.building FROM Buildings JOIN restaurants
        ON Buildings.id = (?)""",(place[-2],)).fetchone()[0]
        # print(location)
        rating = place[-1]

        d[name] = {'category':type, 'building':location,'rating':rating}

    # print(d)

    return d





    pass

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    d = {}
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    data = cur.execute("""SELECT * FROM Categories""").fetchall()
    sorted_data = sorted(data, key=lambda x:x[1])
    for cat in sorted_data:
        count = cur.execute("""SELECT COUNT(category_id) FROM restaurants 
        WHERE category_id = (?)""",(cat[0],)).fetchone()[0]
        d[cat[1]] = count

    # print(d)
    desc_data = sorted(d.items(),key=lambda x:x[1])
    # print(desc_data)
    for i in range(len(desc_data)):
        ax.barh(desc_data[i][0],desc_data[i][1], color='orange', linewidth=3)
    ax.set_xlabel("Category")
    ax.set_ylabel("Counts")
    plt.subplots_adjust(left=0.3)
    fig.savefig("category_graph")
    plt.show()
    return d


    pass

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    l = []
    content = cur.execute("""SELECT restaurants.name, restaurants.rating FROM restaurants JOIN buildings ON
    restaurants.building_id = buildings.id WHERE buildings.building = (?)""",(building_num,)).fetchall()
    content = sorted(content,key=lambda x:x[1], reverse=True)
    for place in content:
        l.append(place[0])

    # print(l)
    return l
    pass

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    data = cur.execute("""SELECT * FROM Categories""").fetchall()
    # print(data)
    l = []
    for type in data:
        average = cur.execute("""SELECT AVG(restaurants.rating) FROM restaurants JOIN categories
            ON restaurants.category_id = categories.id WHERE categories.category = (?)""",
            (type[1],)).fetchone()
        # print(average)
        l.append((type[1],round(average[0],1)))

    l = sorted(l, key=lambda x:x[1])
    # print(l)
    for cat in l:
        ax1.barh(cat[0],cat[1], color='orange', linewidth=3)
    
    ax1.set_xlabel("Average Rating")
    ax1.set_ylabel("Category")

    data2 = cur.execute("""SELECT * FROM Buildings""").fetchall()
    # print(data)
    l2 = []
    for type in data2:
        average = cur.execute("""SELECT AVG(restaurants.rating) FROM restaurants JOIN Buildings
            ON restaurants.building_id = buildings.id WHERE buildings.building = (?)""",
            (type[1],)).fetchone()
        # print(average)
        l2.append((type[1],round(average[0],1)))

    l2 = sorted(l2, key=lambda x:x[1])
    # print(l2)
    for cat in l2:
        ax2.barh(str(cat[0]),cat[1], color='orange', linewidth=3)
    
    ax2.set_xlabel("Average Rating")
    ax2.set_ylabel("Building")

    plt.subplots_adjust(left=0.2)

    fig.savefig("extra_credit_graph")

    plt.show()


    # print(l,l2)

    return [l[-1],l2[-1]]


    







    pass

#Try calling your functions here
def main():
    data = load_rest_data("South_U_Restaurants.db")

    data2 = plot_rest_categories("South_U_Restaurants.db")
    # print(data2)

    data3 = find_rest_in_building(1140,"South_U_Restaurants.db")
    # print(data3)

    get_highest_rating("South_U_Restaurants.db")
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
