import instaloader
from selenium import webdriver
from creds import get_insta_cred, get_hydeauditor_cred
import time
import pandas as pd
from constants import (DRIVER_PATH,
                       INDIVIDUAL_INFLUENCERS_DATA_PATH,
                       INFLUENCERS_NAMES_STORING_PATH,
                       HYPERAUDITOR_URL
                       )

logged_in = False


def login(username, password):
    """
        This function will login to "https://hypeauditor.com/"
    """
    global logged_in
    if not logged_in:
        print("Signing In...")
        browser.get(HYPERAUDITOR_URL)

        # Getting the sign in button & clicking
        signing_btn = browser.find_element_by_xpath(
            "/html/body/div[1]/header/div[2]/div[2]/a[1]")
        signing_btn.click()
        time.sleep(1)

        # Getting the email & password fields &
        # supplying the username & password
        email = browser.find_element_by_name('email')
        email.send_keys(username)

        password_field = browser.find_element_by_name('password')
        password_field.send_keys(password)

        # Getting the login button and clicking
        login_btn = browser.find_element_by_css_selector(
            "button[class='button button-big button-block js-btn-loader']")
        login_btn.click()

        # Finally setting the global logged_in variable
        # to true
        logged_in = True


class Influencer:

    def __init__(self, username=None, report_link=None, followers=None):
        self.username = username
        self.fullname = None
        self.profile_pic_url = None
        self.followers = followers
        self.following = None
        self.age = None
        self.bio = None
        self.total_posts = None
        self.effluence_rate = None
        self.category = None
        self.location = None
        self.website = None
        self.is_verified = False
        self.social_network_links = None

        self.youtube_followers = "No Youtube account"
        self.tiktok_followers = "No Tiktok account"

        self.last_five_post_details = None

        self.insta_bot: instaloader.Instaloader() = None

        # Method callings
        self.insta_username, self.insta_password = get_insta_cred()
        self.hypeauditor_username, self.hypeauditor_password = get_hydeauditor_cred()
        self.__get_effluence_rate(report_link)
        self.__get_details()
        self.__get_age_and_social_links()
        self.__get_post_details()
        self.__write_to_file()

    def __get_effluence_rate(self, report_link):
        """ Scrapes Influencer's effluence rate, category, location
            from https://hypeauditor.com/
         """

        # Signing in to https://hypeauditor.com/
        login(self.hypeauditor_username, self.hypeauditor_password)
        print("Login successful")

        time.sleep(1)
        print("Getting data from hyperauditor.com...")
        browser.get(report_link)

        # Getting the location
        location = browser.find_elements_by_xpath(
            "/html/body/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[4]/span")
        self.location = location[0].text[2:]

        # Getting the effluence_rate
        effluence_rate = browser.find_elements_by_xpath(
            "/html/body/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[2]")
        self.effluence_rate = effluence_rate[0].text

        # Getting Influencer's categories
        category = browser.find_elements_by_css_selector(
            "div[class='kyb-user-info--topic']")
        self.category = " ".join(cat.text for cat in category)

        # Getting Tiktok and Youtube Followers
        social_links = browser.find_elements_by_css_selector(
            'ul[class="report-profile-tabs--list"]')
        for i in range(len(social_links)):
            link = social_links[i].find_elements_by_tag_name('li')
            for j in range(len(link)):
                if link[j].get_attribute("data-type") == 'tiktok':
                    tik_tok = link[j].text
                    self.tiktok_followers = tik_tok.split("\n")[1]

                if link[j].get_attribute("data-type") == 'youtube':
                    youtube = link[j].text
                    self.youtube_followers = youtube.split("\n")[1]

        print("Finished!")

    def __get_the_insta_bot(self):
        """
            Creates an insta bot and logins to it
        """
        if self.insta_bot is None:
            bot = instaloader.Instaloader(
                download_videos=False, download_video_thumbnails=False
            )

            # trying to login
            try:
                bot.login(self.insta_username, self.insta_password)
            except Exception as e:
                print(e.message)

            self.insta_bot = bot
            return
        bot = instaloader.Instaloader(
            download_videos=False, download_video_thumbnails=False
        )
        self.insta_bot = bot

    def __get_details(self):
        """ Get an Influencer's details
        from Instagram """

        print("Getting influencer's data from Instagram...")

        self.__get_the_insta_bot()
        ig_user = instaloader.Profile.from_username(
            self.insta_bot.context, self.username)
        self.fullname = ig_user.full_name
        self.bio = ig_user.biography
        self.following = ig_user.followees
        self.total_posts = ig_user.mediacount
        self.is_verified = ig_user.is_verified
        self.profile_pic_url = ig_user.profile_pic_url
        self.website = ig_user.external_url
        print("Finished!")

    def __get_age_and_social_links(self):
        """ Scrapes given influence's age,
        social media links from Google """

        # Searching and adding Influencer's age from
        # Google
        print("Getting data from google.com...")
        browser.get(f"https://www.google.com/search?q={self.username} age")

        birth_info = browser.find_element_by_css_selector(
            "div[class='Z0LcW XcVN5d']")
        self.age = birth_info.text[:2]

        # Getting the avaliable social media links and adding
        # them to Influencer's "social_links"
        social_links_data = browser.find_elements_by_css_selector(
            "div[class='PZPZlf dRrfkf kno-vrt-t']")
        social_links = [(link.text, link.find_element_by_tag_name(
            'a').get_attribute('href')) for link in social_links_data]
        self.social_network_links = social_links
        print("Finished!")

    def __get_post_details(self):
        """Gets Influencer's last 5 Image's Posts with details"""

        print("Getting recent 5 image's posts with details...")

        # Setting the bot for the Influencer
        self.__get_the_insta_bot()
        u = instaloader.Profile.from_username(
            self.insta_bot.context, self.username)

        # Grabbing the posts setting it to "last_five_posts_details"
        i = 1
        post_details = {}
        for post in u.get_posts():
            if i != 6:
                post_details.update({post.shortcode:
                                     {
                                         'description': post.pcaption,
                                         'hashtags': " ".join([f"#{pc}" for pc in post.caption_hashtags if pc != ""]),
                                         'likes': post.likes,
                                         'comments': post.comments,
                                         'post URL': f"https://www.instagram.com/p/{post.shortcode}",
                                         'media URL': post.url}})
                i += 1
            else:
                break
        self.last_five_post_details = post_details
        print("Finished!")

    def __write_to_file(self):
        """
        Writes the Influencer's data
        in an excel sheet
        """
        print("Writeing to file...")

        # "df" for Influencer's info
        df = pd.DataFrame(data={
            'username': self.username,
            'name': self.fullname,
            'age': self.age,
            'location': self.location,
            'category': self.category,
            'effluence Rate': self.effluence_rate,
            'bio': self.bio,
            'profile Pic URL': self.profile_pic_url,
            'followers': self.followers,
            'following': self.following,
            'total Posts': self.total_posts,
            'website': self.website,
            "verified": self.is_verified,
            "tikTok Followers": str(self.tiktok_followers),
            "youtube Followers": str(self.youtube_followers),
            "social Networks": "".join([f"{link}, " for link in self.social_network_links])
        }, index=[0])

        # "df2" for Influencer's last 5 post details
        df2 = pd.DataFrame(data=[details for post, details in self.last_five_post_details.items()
                                 ])

        # Writting to an xlsx file
        file_name = f"{INDIVIDUAL_INFLUENCERS_DATA_PATH}{self.username}.xlsx"
        with pd.ExcelWriter(file_name) as writer:
            df.to_excel(
                writer, sheet_name=f"{self.username} Details", index=False)
            df2.to_excel(
                writer, sheet_name=f"{self.username} Posts", index=False)
            writer.save()

        print("Finished!")


# Driver Code
if __name__ == "__main__":

    browser = webdriver.Chrome(DRIVER_PATH)

    with open(INFLUENCERS_NAMES_STORING_PATH + "Influencer_data.txt", 'r') as f:
        for i in range(1, 6):
            entry = f.readline().split(',')
            uname = entry[0].split(":")[1]
            r_page = entry[1][13:]
            followers = entry[2].split(":")[1]
            print(f"{uname} {r_page} {followers}")

            infl = Influencer(
                username=uname, report_link=r_page, followers=followers)

    browser.quit()
