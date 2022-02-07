def find_followers_and_id(root):
    '''
    function return followers address of a user(friends) in a list
    users_id = [0xffffAAAA, 0xbbbbcccc, 0xddddeeee]
    users_followers = [0xffffAAAA, 0xbbbbcccc, 0xddddeeee] followers address el kelma nfsha
    '''
    users = root.children
    users_id = []
    users_followers = []
    for user in users: #O[x*y] where x is number of users and y is number of children of each user
        for e in user.children:
            if e.data == "<id>":
                users_id.append(e)
            if e.data == "<followers>":
                users_followers.append(e)
    return users_id, users_followers

#traverse and get leaf nodes
def printer(element, l): #aT(n/b) + O[n^d] as we traverse in the tree logn
    if len(element.children) == 0:
        # print(element.data)
        l.append(element.data)
        return
    else:
        for e in element.children:
            printer(e, l)