import json

# If the data dump has no issues in it
# For displaying user data
def display_userdata(file):
    with open(file, "r") as f:
        data=json.load(f)
    print("User information\n")
    for user in data["users"]:
        print(f"ID-{user["id"]}: {user["name"]} is friend with {user["friends"]} and liked pages {user["liked_pages"]}")
    print("\n")
    print("Page information\n")
    for page in data["pages"]:
        print(f"{page["id"]}-{page["name"]}")

delhi_coders=display_userdata("massive_data.json")
print(delhi_coders)

# Data Cleaning
def clean_data(data):
    #to remove those users which have no name
    data['users']=[user for user in data['users'] if user['name'].strip()]

    #to fix inconsistent data
    data["users"]=[user for user in data["users"] if user['friends'] or user['liked_pages']]

    #to fix duplicate values in user data
    for user in data["users"]:
        user["friends"]=list(set(user["friends"]))
        user["liked_pages"]=list(set(user["liked_pages"]))

    unique_page={}
    for page in data["pages"]:
        unique_page[page["id"]]=page
        data['pages']=list(unique_page.values())
    return data

with open("massive_data.json", "r") as f:
    data=json.load(f)
data=clean_data(data)
json.dump(data, open("massive_data.json","w"), indent=4)

# People you may like feature
import json
def load_data(filename):
    with open(filename, "r") as f:
        data=json.load(f)
    return data
def people_you_may_know(user_id, data):
    user_friends={}
    for user in data["users"]:
        user_friends[user["id"]]=set(user['friends'])
    if user_id not in user_friends:
        return []
    direct_friends=user_friends[user_id]
    # with this suggestions dictionary we will get id and score pair
    suggestions={}
    for friends in direct_friends:
        #the friend should exist in user_friends dictionary also
        if friends in user_friends:
            for mutual in user_friends[friends]:
                if mutual!=user_id and mutual not in direct_friends:
                    suggestions[mutual]=suggestions.get(mutual, 0)+1
    #those who have much higher score will be first and the least will be at the last that's why descending order 
    sorted_suggestions=sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
    return [user_id for user_id, score in sorted_suggestions]
data=load_data("massive_data.json")
print(people_you_may_know(1,data))

# Pages you might like feature
import json 
def pages_you_may_like(user_id, data):
    user_pages={}
    # pages are stored here on the basis of the id of the user
    for user in data['users']:
        user_pages[user['id']]=set(user['liked_pages'])
    if user_id not in user_pages:
        return []
    user_liked_pages=user_pages[user_id]
    # here the suggestion dictionary will contain page_id score pair
    suggestions={}
    for other_user, pages in user_pages.items():
        # common liked pages between both users
        shared_common_pages=user_liked_pages.intersection(pages)
        for page in pages:
            # page and score pair
            if page not in user_liked_pages:
                suggestions[page]=suggestions.get(page,0)+len(shared_common_pages)
    # sorting the data in descending order according to the score
    sorted_suggestions=sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
    return [page_id for page_id, _ in sorted_suggestions]
data=load_data("massive_data.json")
user_id=6
suggested_pages=pages_you_may_like(user_id, data)
print(suggested_pages)