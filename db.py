from couchdb import Server
import time
server = Server()
db = server['blogs']


def create_blog(title):
    return db.save({"title":title,
                   "content":"",
                   "tags":"",
                   "url":"",
                   "published":False,
                   "time":time.time()})[0]

def update_values(keys, values, _id):
    new = get_blog_entry(_id)
    for value,key in zip(values,keys):
        new[key] = value
    return db.save(new)



def add_revision(content, message_to_save_with, _id):
    to_append = {"content":content,"commit_message":message_to_save_with,"time":time.time()}
    blog = get_blog_entry(_id)
    blog["revisions"] += to_append
    update_values(["revisions"], [blog["revisions"],], _id)
    return
    
def list_blog_info_from_tags(attrs):
    s = ""
    for att in attrs:
        s += "doc."+att+", "
    s = s[:-2]
    map_fun = 'function(doc) {emit(['+s+'],doc._id);}'
    results = db.query(map_fun)
    ret = [blog.get("key") for blog in results]
    to_ret = []
    for r in ret:
        dic = {}
        for k,attr in enumerate(attrs):
            dic[attr] = r[k]
        to_ret.append(dic)
    return to_ret

def get_id(url):
    map_fun = "function(doc) {if (doc.url == '"+url+"')emit(doc._id, null);}"
    for row in db.query(map_fun):
        return row.key


def list_blogs_all():
    attrs = ["title", "tags", "time","revisions","_id"]
    return list_blog_info_from_tags(attrs)

def list_blogs_meta():
    attrs = ["title", "time", "_id", "tags"]
    return list_blog_info_from_tags(attrs)
    

def get_blog_entry(_id):
    old_doc = db[_id]
    new = {}
    for x in old_doc:
        new[x] = old_doc[x]
    return new

