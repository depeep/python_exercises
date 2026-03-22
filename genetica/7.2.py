class Superstar:
    def __init__(self, real, nick, hit):
        self.__real_name = real
        self.__nick_name = nick
        self.__latest_hit = hit

    def get_real_name(self):
        return self.__real_name

    def get_nick_name(self):
        return self.__nick_name

    def set_nick_name(self, new_nick_name):
        self.__nick_name = new_nick_name

    def get_latest_hit(self):
        return self.__latest_hit

    def set_latest_hit(self, new_hit):
        self.__latest_hit = new_hit

    def get_latest_hit(self):
        return self.__latest_hit

def show_latest_hit(star):
    name = star.get_real_name()
    nick = star.get_nick_name()
    hit =  star.get_latest_hit()
    print('The latest hit of', nick, '(' + name + ') is: "' + hit + '"')

def main():
    star1 = Superstar('Britney Spears', 'Queen B', 'Baby One more Time')
    star2 = Superstar('Justin Bieber', 'JB', 'What Do You Mean?')
    print()
    show_latest_hit(star1)
    show_latest_hit(star2)

    star1.set_latest_hit('Hold Me Closer')
    star2.set_latest_hit('Honest')
    print()
    show_latest_hit(star1)
    show_latest_hit(star2)

main()

"""mY PREDICTION: There will be some sort of error, because there is no method defined for set_real_name
I was wrong, apparently it was set during init"""