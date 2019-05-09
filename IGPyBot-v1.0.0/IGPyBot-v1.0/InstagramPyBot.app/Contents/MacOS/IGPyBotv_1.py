import os
import time
import sys
from src import InstaBot
from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.unfollow_protocol import unfollow_protocol

##[1 username, 2 pwd, 3 follows/day, 4  followtime,5 likeperday, 6 likesperhashtag,7 blacklistuname, 8 blacklist hashtags
## 9 comments per day, 10 hashtaglist, 11 commentlist, 12 unfollowsperday]
def main():
    for i in sys.argv:
        print i
    bot = InstaBot(
        login=sys.argv[1],
        password=sys.argv[2],
        like_per_day=sys.argv[5],
        comments_per_day=sys.argv[9],
        tag_list=sys.argv[10],
        tag_blacklist=sys.argv[8],
        user_blacklist={},
        max_like_for_one_tag=sys.argv[6],
        follow_per_day=sys.argv[3],
        follow_time=sys.argv[4],
        unfollow_per_day=sys.argv[12],
        unfollow_break_min=15,
        unfollow_break_max=30,
        log_mod=0,
        proxy='',
        # List of list of words, each of which will be used to generate comment
        # For example: "This shot feels wow!"
        comment_list= sys.argv[11].strip().split(','),
        # Use unwanted_username_list to block usernames containing a string
        ## Will do partial matches; i.e. 'mozart' will block 'legend_mozart'
        ### 'free_followers' will be blocked because it contains 'free'
        unwanted_username_list=sys.argv[7].strip().split(','),
        unfollow_whitelist=[])
    while True:

        #print("# MODE 0 = ORIGINAL MODE BY LEVPASHA")
        #print("## MODE 1 = MODIFIED MODE BY KEMONG")
        #print("### MODE 2 = ORIGINAL MODE + UNFOLLOW WHO DON'T FOLLOW BACK")
        #print("#### MODE 3 = MODIFIED MODE : UNFOLLOW USERS WHO DON'T FOLLOW YOU BASED ON RECENT FEED")
        #print("##### MODE 4 = MODIFIED MODE : FOLLOW USERS BASED ON RECENT FEED ONLY")
        #print("###### MODE 5 = MODIFIED MODE : JUST UNFOLLOW EVERYBODY, EITHER YOUR FOLLOWER OR NOT")

        ################################
        ##  WARNING   ###
        ################################

        # DON'T USE MODE 5 FOR A LONG PERIOD. YOU RISK YOUR ACCOUNT FROM GETTING BANNED
        ## USE MODE 5 IN BURST MODE, USE IT TO UNFOLLOW PEOPLE AS MANY AS YOU WANT IN SHORT TIME PERIOD

        mode = 0

        #print("You choose mode : %i" %(mode))
        #print("CTRL + C to cancel this operation or wait 30 seconds to start")
        #time.sleep(30)

        if mode == 0:
            bot.new_auto_mod()

        elif mode == 1:
            check_status(bot)
            while bot.self_following - bot.self_follower > 200:
                unfollow_protocol(bot)
                time.sleep(10 * 60)
                check_status(bot)
            while bot.self_following - bot.self_follower < 400:
                while len(bot.user_info_list) < 50:
                    feed_scanner(bot)
                    time.sleep(5 * 60)
                    follow_protocol(bot)
                    time.sleep(10 * 60)
                    check_status(bot)

        elif mode == 2:
            bot.bot_mode = 1
            bot.new_auto_mod()

        elif mode == 3:
            unfollow_protocol(bot)
            time.sleep(10 * 60)

        elif mode == 4:
            feed_scanner(bot)
            time.sleep(60)
            follow_protocol(bot)
            time.sleep(10 * 60)

        elif mode == 5:
            bot.bot_mode = 2
            unfollow_protocol(bot)

        else:
            print("Wrong mode!")

if __name__ == '__main__':
    main()
