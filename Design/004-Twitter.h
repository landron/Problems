/*

My solution: TwitterMine

Runtime
15ms
Beats   22.94%
Memory
63.42MB
Beats   5.11%

* Massive Over-Caching (Memory Bottleneck): Storing a dedicated std::list<int>
feed
* Redundant Merging & Linear Scans (Runtime Bottleneck): In your add_user_tweets
method, you loop through a list
*/
#pragma once

#include <cassert>
#include <list>
#include <unordered_map>
#include <vector>

class TwitterMine {
  private:
    struct User;
    using Users = std::unordered_map<int, User>;
    using UserConnections = std::unordered_map<int, Users::iterator>;

    struct User {
        UserConnections followers;
        UserConnections followed;

        std::list<int> tweets_order;
        std::unordered_map<int, std::list<int>::iterator> tweets;
        std::list<int> feed;
    };
    static constexpr size_t RECENT_TWEETS = 10;

  public:
    void postTweet(int userId, int tweetId) {
        auto [user, _] = users.insert({userId, User{}});
        m_tweets[tweetId] = m_tweets.size();
        user->second.tweets_order.push_front(tweetId);
        user->second.tweets[tweetId] = user->second.tweets_order.begin();

        auto update_feed = [](Users::iterator it, int tweetId) {
            auto& feed = it->second.feed;
            feed.push_front(tweetId);
            if (feed.size() > RECENT_TWEETS) feed.pop_back();
        };

        for (auto it : user->second.followers) {
            update_feed(it.second, tweetId);
        }
        // user follows user itself
        update_feed(user, tweetId);
    }

    std::vector<int> getNewsFeed(int userId) {
        auto user = users.find(userId);
        if (user == users.end()) return {};

        auto convert = [](const std::list<int>& l) -> std::vector<int> {
            return {l.begin(), l.end()};
        };
        return convert(user->second.feed);
    }

    void follow(int followerId, int followeeId) {
        assert(followerId != followeeId && "constraint");

        auto [follower, _] = users.insert({followerId, User{}});
        auto [followee, _] = users.insert({followeeId, User{}});
        auto& followers = followee->second.followers;
        // already followed
        if (followers.find(followerId) != followers.end()) return;
        followers[followerId] = follower;
        follower->second.followed[followeeId] = followee;

        add_user_tweets(follower->second, followee->second);
    }

    void unfollow(int followerId, int followeeId) {
        // assert(followerId != followeeId && "constraint");
        if (followerId == followeeId) return;

        auto follower = users.find(followerId);
        auto followee = users.find(followeeId);
        if (follower == users.end() || followee == users.end()) return;

        auto& followers = followee->second.followers;
        auto it = followers.find(followerId);
        // not followed
        if (it == followers.end()) return;
        followers.erase(it);
        auto& followed = follower->second.followed;
        it = followed.find(followeeId);
        assert(it != followed.end() && "followee followed");
        followed.erase(it);

        remove_user_tweets(follower->second, followee->second);

        // repopulate feed from followed
        repopulate_feed(follower->second);
    }

  private:
    void remove_user_tweets(User& follower, const User& followee) {
        auto& feed = follower.feed;
        auto& tweets = followee.tweets;

        if (tweets.empty()) return;

        auto full_feed = feed.size() == RECENT_TWEETS;
        for (auto it = feed.begin(); it != feed.end();)
            if (tweets.find(*it) != tweets.end()) it = feed.erase(it);
            else ++it;
        if (!full_feed || (feed.size() == RECENT_TWEETS)) return;
    }

    void add_user_tweets(User& follower, const User& followee) {
        auto& feed = follower.feed;
        auto& tweets = followee.tweets_order;

        auto insert = [&](std::list<int>& l, int tweetId) -> bool {
            assert(l.size() <= RECENT_TWEETS);

            auto to_add = m_tweets[tweetId];

            // early break
            if (l.size() == RECENT_TWEETS && (m_tweets[l.back()] > to_add))
                return false;

            if (l.empty()) {
                l.push_front(tweetId);
                return true;
            }
            auto next = m_tweets[*l.begin()];
            if (next == to_add) return true;
            if (next < to_add) {
                l.push_front(tweetId);
                if (l.size() > RECENT_TWEETS) l.pop_back();
                return true;
            }

            for (auto it = std::next(l.begin()); it != l.end(); ++it) {
                next = m_tweets[*it];
                if (next == to_add) return true;
                if (next < to_add) {
                    l.insert(it, tweetId);
                    if (l.size() > RECENT_TWEETS) l.pop_back();
                    return true;
                }
            }
            if (l.size() != RECENT_TWEETS) l.push_back(tweetId);
            return (l.size() != RECENT_TWEETS);
        };

        for (auto it = tweets.begin(); it != tweets.end(); ++it) {
            if (!insert(feed, *it)) break;
        }
    }

    void repopulate_feed(User& user) {
        auto& feed = user.feed;
        // feed not changed
        if (feed.size() == RECENT_TWEETS) return;
        for (auto u : user.followed)
            add_user_tweets(user, u.second->second);
        // also add from itself
        add_user_tweets(user, user);
    }

  private:
    std::unordered_map<int, User> users;
    // tweet ID => order number
    std::unordered_map<int, size_t> m_tweets;
};
