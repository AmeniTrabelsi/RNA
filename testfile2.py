import pickle

favorite_color = {"lion": "yellow", "kitty": "red"}

pickle.dump(favorite_color, open("save.p", "wb"))
# favorite_color2 = pickle.load( open( "save.p", "rb" ) )
# print favorite_color2
