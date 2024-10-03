import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from consts import USERNAME, PASSWORD

def get_follower_details(username, password):
    url = 'https://www.instagram.com/'
    driver = webdriver.Firefox()

    driver.get(url)
    # Wait for the username field to be present and send the username
    cookies = pickle.load(open('cookies.pkl', 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)

    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(USERNAME)
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(PASSWORD)
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._acan._acap._acas._aj1-._ap30'))).click() #login button
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button._a9--:nth-child(2)'))).click() #not now button

    pickle.dump(driver.get_cookies(), open('cookies.pkl', 'wb'))

    time.sleep(5) # wait for the page to load

    # Define the JavaScript code to retrieve followers and followings
    script = """
    const username = 'andrew.howee';

    let followers = [];
    let followings = [];
    let dontFollowMeBack = [];
    let iDontFollowBack = [];

    return (async () => {
    try {
        console.log(`Process started! Give it a couple of seconds`);

        const userQueryRes = await fetch(
        `https://www.instagram.com/web/search/topsearch/?query=${username}`
        );

        const userQueryJson = await userQueryRes.json();

        const userId = userQueryJson.users.map(u => u.user)
                                        .filter(
                                            u => u.username === username
                                        )[0].pk;

        let after = null;
        let has_next = true;

        while (has_next) {
        await fetch(
            `https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=` +
            encodeURIComponent(
                JSON.stringify({
                id: userId,
                include_reel: true,
                fetch_mutual: true,
                first: 50,
                after: after,
                })
            )
        )
            .then((res) => res.json())
            .then((res) => {
            has_next = res.data.user.edge_followed_by.page_info.has_next_page;
            after = res.data.user.edge_followed_by.page_info.end_cursor;
            followers = followers.concat(
                res.data.user.edge_followed_by.edges.map(({ node }) => {
                return {
                    username: node.username,
                    full_name: node.full_name,
                };
                })
            );
            });
        }

        console.log({ followers });

        after = null;
        has_next = true;

        while (has_next) {
        await fetch(
            `https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=` +
            encodeURIComponent(
                JSON.stringify({
                id: userId,
                include_reel: true,
                fetch_mutual: true,
                first: 50,
                after: after,
                })
            )
        )
            .then((res) => res.json())
            .then((res) => {
            has_next = res.data.user.edge_follow.page_info.has_next_page;
            after = res.data.user.edge_follow.page_info.end_cursor;
            followings = followings.concat(
                res.data.user.edge_follow.edges.map(({ node }) => {
                return {
                    username: node.username,
                    full_name: node.full_name,
                };
                })
            );
            });
        }

        console.log({ followings });

        dontFollowMeBack = followings.filter((following) => {
        return !followers.find(
            (follower) => follower.username === following.username
        );
        });

        console.log({ dontFollowMeBack });

        iDontFollowBack = followers.filter((follower) => {
        return !followings.find(
            (following) => following.username === follower.username
        );
        });

        console.log({ iDontFollowBack });

        return {
        followers: followers,
        followings: followings,
        dontFollowMeBack: dontFollowMeBack,
        iDontFollowBack: iDontFollowBack
        };
    } catch (err) {
        console.log({ err });
        return null;
    }
    })();
    """

    # Execute the main script and capture the results
    results = driver.execute_script(script)

    followers = results['followers']
    followings = results['followings']
    dont_follow_me_back = results['dontFollowMeBack']
    i_dont_follow_back = results['iDontFollowBack']

    print("script is complete.")
    driver.close()
    return followers, followings, dont_follow_me_back, i_dont_follow_back

if __name__ == '__main__':
    followers, followings, dont_follow_me_back, i_dont_follow_back = get_follower_details(USERNAME, PASSWORD)
    print(dont_follow_me_back)